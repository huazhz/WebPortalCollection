# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import os
import json
import re
import time
import traceback
import jieba

from NewsDB.models import News, NewsToLimitTags, NewsToTags


# 路径准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'temp')


# 数据准备
news_item = ['title', 'url', 'kind', 'hot_rate', 'date', 'img_url']

pattern_news_dict = {
    'title': r'^.{1,100}$',
    'url': r'^.{1,200}$',
    'kind': r'^.{1,50}$',
    'hot_rate': r'^[.0-9]{1,50}$',
    'date': r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    'img_url': r'^.{0,300}$',
}

kind_item = [
    '资讯',
    '军事',
    '体育',
    '娱乐',
    '时政',
    '国际',
    '财经',
    '时尚',
    '汽车',
    '房产',
    '游戏',
    '社会',
    '教育',
    '旅游',
    '科技',
]

with open(os.path.join(TMP_DIR, 'stopword.txt'), 'rb') as stop_f:
    stop_words = set([line.strip() for line in stop_f if line.strip()])

jieba.initialize()


# 功能函数
def check_date(date):
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


# 响应函数
def insert_news(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        all_data = json.loads(request.body)
        news_dict = all_data['News']
        news_limit_tags = all_data['NewsToLimitTags']
        news_tags = all_data['NewsToTags']
        check_pwd = all_data['pwd']
        if check_pwd != 'meng835542226':
            result['retcode'] = 403
            result['error_msg'] = 'xxxxxx'
        else:
            if len(news_dict) > 2000:
                result['retcode'] = 10011
                result['error_msg'] = 'too many news to insert'
            else:
                save_list = []
                limit_list = []
                unlimit_list = []
                ac_insert = []
                for url, news in news_dict.iteritems():
                    if url != news['url']:
                        continue
                    re_flag = True
                    for i in xrange(len(news_item)):
                        if news_item[i] != 'hot_rate':
                            if not re.match(pattern_news_dict[news_item[i]], news[news_item[i]]):
                                re_flag = False
                                break
                        else:
                            try:
                                hot_str = str(news['hot_rate'])
                                if not re.match(pattern_news_dict['hot_rate'], hot_str):
                                    re_flag = False
                                    break
                            except:
                                re_flag = False
                                break
                        
                    if re_flag:
                        re_flag = check_date(news['date'])
                        
                    if re_flag:
                        check_set = News.objects.filter(url=news['url'])
                        if check_set.exists():
                            check_set[0].hot_rate = news['hot_rate']
                            check_set[0].save(update_fields=['hot_rate'])
                            continue
                            
                    if re_flag:
                        save_list.append(News(
                            title=news['title'],
                            url=news['url'],
                            kind=news['kind'],
                            hot_rate=news['hot_rate'],
                            date=news['date'],
                            img_url=news['img_url']
                        ))
                        ac_insert.append(news['url'])
                for t_url, t_tag_list in news_limit_tags.iteritems():
                    if t_url not in ac_insert:
                        continue
                    if not re.match(pattern_news_dict['url'], t_url):
                        continue
                    for t_tag in t_tag_list:
                        if not re.match(pattern_news_dict['kind'], t_tag):
                            continue
                        limit_list.append(
                            NewsToLimitTags(
                                url=t_url,
                                tag=t_tag
                            )
                        )
                for t_url, t_tag_list in news_tags.iteritems():
                    if t_url not in ac_insert:
                        continue
                    if not re.match(pattern_news_dict['url'], t_url):
                        continue
                    for t_tag in t_tag_list:
                        if not re.match(pattern_news_dict['kind'], t_tag):
                            continue
                        unlimit_list.append(
                            NewsToTags(
                                url=t_url,
                                tag=t_tag
                            )
                        )
                News.objects.bulk_create(save_list)
                NewsToLimitTags.objects.bulk_create(limit_list)
                NewsToTags.objects.bulk_create(unlimit_list)
                result['error_msg'] = 'insert %d news' % len(save_list)
                result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def all_news(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        all_set = News.objects.all()
        result['news'] = [news.to_dict() for news in all_set]
        result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


# def clean_news(request):
#     result = {
#         'retcode': 10000,
#         'error_msg': '',
#     }
    
#     try:
#         News.objects.all().delete()
#         result['retcode'] = 0
#     except:
#         print traceback.format_exc()
#         result['retcode'] = 10010
#         result['error_msg'] = traceback.format_exc()
#     return HttpResponse(json.dumps(result), content_type='application/json')


def news(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        all_data = json.loads(request.body)
        p_kind = all_data['kind']
        p_head = int(all_data['head'])
        p_tail = int(all_data['tail'])
        if p_kind == 'all':
            news_set = News.objects.all().order_by('-hot_rate')[p_head: p_tail]
            result['news'] = [news.to_dict() for news in news_set]
            result['retcode'] = 0
        elif p_kind in kind_item:
            news_set = News.objects.filter(kind=p_kind).order_by('-hot_rate')[p_head: p_tail]
            result['news'] = [news.to_dict() for news in news_set]
            result['retcode'] = 0
        else:
            result['retcode'] = 10003
            result['retcode'] = 'illegal tags'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def query(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        all_data = json.loads(request.body)
        p_query = all_data['query']
        seg_list = list(set(jieba.cut_for_search(p_query)) - stop_words)
        url_hit_dict = {}
        for t_tag in seg_list:
            query_set = NewsToTags.objects.filter(tag=t_tag)
            for news_tag in query_set:
                if news_tag.url in url_hit_dict:
                    url_hit_dict[news_tag.url] += 1
                else:
                    url_hit_dict[news_tag.url] = 1
        sorted_list = sorted(url_hit_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        hit2url = {}
        for t_url, t_hit in sorted_list:
            if t_hit in hit2url:
                hit2url[t_hit].append(t_url)
            else:
                hit2url[t_hit] = [t_url]
        return_news = []
        news_set = News.objects.filter(url__in=[t_sor[0] for t_sor in sorted_list]).order_by('-hot_rate')
        hit_count_list = sorted(hit2url.keys(), reverse=True)
        for hit_count in hit_count_list:
            for p_news in news_set.iterator():
                if p_news.url in hit2url[hit_count]:
                    return_news.append(p_news.to_dict())
        result['news'] = return_news
        result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')
