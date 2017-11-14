# -*- coding: utf-8 -*-
"""
timer for uwsgi app
"""
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsManager.settings")

import time
from uwsgidecorators import timer, cron

from NewsDB.models import News, NewsToLimitTags, NewsToTags
from UserDB.models import UserToKind
from NewsRecommendSys.models import UserToTags, UserToDateTitle, UserToReadUrl, UserToRecommendUrl

from ExpandFunction.userRecommendNews import recommendNews
from ExpandFunction.addUserTags import addUserTags

# 路径准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@cron(0, 2, -1, -1, -1, target='spooler')
def clean_loss_session(num):
    """
    清理过期的session
    """
    print "it's 2:00 in the morning: cleaning useless django_session"
    os.system('python manage.py clearsessions')


@cron(30, 2, -1, -1, -1, target='spooler')
def update_user_tags(num):
    """
    更新用户感兴趣标签
    """
    print "it's 2:30 in the morning: update UserToTags_db"
    user_tags = {}
    old_tag_set = UserToTags.objects.all()
    for tag_info in old_tag_set.iterator():
        if tag_info.user_name in user_tags:
            user_tags[tag_info.user_name].append([tag_info.tag, tag_info.weight])
        else:
            user_tags[tag_info.user_name] = [[tag_info.tag, tag_info.weight]]
    one_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*1))
    two_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*2))
    three_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*3))
    four_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*4))
    five_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*5))
    date_list = [one_date_str, two_date_str, three_date_str, four_date_str, five_date_str]
    day_records = []
    for date_str in date_list:
        title_set = UserToDateTitle.objects.filter(date=date_str)
        day_dict = {}
        for title_info in title_set.iterator():
            if title_info.user_name in day_dict:
                day_dict[title_info.user_name].append(title_info.title)
            else:
                day_dict[title_info.user_name] = [title_info.title]
        day_records.append(day_dict)
    new_dict = addUserTags(user_tags, day_records, 'temp/stopword.txt')
    new_set = []
    for username, tags in new_dict.iteritems():
        for t_tag, t_weight in tags:
            new_set.append(
                UserToTags(
                    tag=t_tag,
                    user_name=username,
                    weight=t_weight
                )
            )
    UserToTags.objects.all().delete()
    UserToTags.objects.bulk_create(new_set)


@cron(0, 3, -1, -1, -1, target='spooler')
def clean_database(num):
    """
    清理超过时限的新闻数据和用户数据
    """
    title_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*5))
    print "it's 3:00 in the morning: cleaning UserToDateTitle_db to %s" % title_date_str
    UserToDateTitle.objects.filter(date__lte=title_date_str).delete()

    out_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*3))
    delete_news_set = News.objects.filter(date__lte=out_date_str)
    delete_url_list = list(delete_news_set.values_list('url', flat=True))

    print "it's 3:00 in the morning: cleaning UserToReadUrl_db to %s" % out_date_str
    UserToReadUrl.objects.filter(url__in=delete_url_list).delete()

    print "it's 3:00 in the morning: cleaning NewsToTags_db to %s" % out_date_str
    NewsToTags.objects.filter(url__in=delete_url_list).delete()

    print "it's 3:00 in the morning: cleaning NewsToLimitTags_db to %s" % out_date_str
    NewsToLimitTags.objects.filter(url__in=delete_url_list).delete()

    print "it's 3:00 in the morning: cleaning News_db to %s" % out_date_str
    delete_news_set.delete()


@timer(3600, target='spooler')
def update_user_fc(signum):
    """
    更新用户感兴趣的新闻链接表
    """
    news_set = News.objects.all()
    news_rate = {}
    news_kind = {}
    for news in news_set.iterator():
        news_rate[news.url] = news.hot_rate
        news_kind[news.url] = news.kind
    
    user_kind_set = UserToKind.objects.all()
    user_kind = {}
    for user2kind in user_kind_set.iterator():
        if user2kind.user_name in user_kind:
            user_kind[user2kind.user_name].append(user2kind.kind)
        else:
            user_kind[user2kind.user_name] = [user2kind.kind]
    
    user_tag_set = UserToTags.objects.all()
    user_tag2rate = {}
    tag_users = {}
    user_tags = {}
    for tag_info in user_tag_set.iterator():
        if tag_info.user_name in user_tag2rate:
            user_tag2rate[tag_info.user_name].append([tag_info.tag, tag_info.weight])
            user_tags[tag_info.user_name].append(tag_info.tag)
        else:
            user_tag2rate[tag_info.user_name] = [[tag_info.tag, tag_info.weight]]
            user_tags[tag_info.user_name] = [tag_info.tag]
        if tag_info.tag in tag_users:
            tag_users[tag_info.tag].append(tag_info.user_name)
        else:
            tag_users[tag_info.tag] = [tag_info.user_name]

    user_url_set = UserToReadUrl.objects.all()
    user_record = {}
    for user_url in user_url_set.iterator():
        if user_url.user_name in user_record:
            user_record[user_url.user_name].append(user_url.url)
        else:
            user_record[user_url.user_name] = [user_url.url]

    news_tag_set = NewsToLimitTags.objects.all()
    news_tag = {}
    for news_tg in news_tag_set.iterator():
        if news_tg.url in news_tag:
            news_tag[news_tg.url].append(news_tg.tag)
        else:
            news_tag[news_tg.url] = [news_tg.tag]

    user_recommend_url = recommendNews(news_rate, news_kind, user_kind, user_tag2rate, tag_users, user_tags, user_record, news_tag)
    
    now_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print "it's %s, delete all old user recommend from UserToRecommendUrl_db" % now_time_str
    print "now add new data to UserToRecommendUrl_db"
    add_recommend_list = []
    for t_user, url_list in user_recommend_url.iteritems():
        for t_url in url_list:
            add_recommend_list.append(
                UserToRecommendUrl(
                    url=t_url,
                    user_name=t_user,
                )
            )
    UserToRecommendUrl.objects.bulk_create(add_recommend_list)
    finish_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print "it's %s, finish update UserToRecommendUrl_db" % finish_time_str
