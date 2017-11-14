# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import os
import json
import re
import time
import traceback

from NewsDB.models import News
from UserDB.models import Member, UserToKind
from NewsRecommendSys.models import UserToRecommendUrl

# 路径准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'temp')

# 数据准备
user_item = ['nick_name', 'user_name', 'password']

pattern_user_dict = {
    'nick_name': r'^.{1,14}$',
    'user_name': r'^.{6,14}$',
    'password': r'^.{6,14}$',
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

kind_item_set = set(kind_item)


# 功能函数
def check_user_cookie(request):
    try:
        if request.session['user_name']:
            request.session.set_expiry(604800)
            return True
    except:
        pass
    return False


# 响应函数
def sign_up(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        user = json.loads(request.body)
        re_flag = True
        for i in xrange(len(user_item)):
            if not re.match(pattern_user_dict[user_item[i]], user[user_item[i]]):
                re_flag = False
                result['retcode'] = 10003
                result['error_msg'] = 'error in %s' % user_item[i]
                break
            
        if re_flag:
            check_set = Member.objects.filter(user_name=user['user_name'])
            if check_set.exists():
                re_flag = False
                result['retcode'] = 10001
                result['error_msg'] = 'user existed'
        
        if re_flag:
            add_kind = []
            add_recommend = []
            for p_kind in kind_item:
                add_kind.append(
                    UserToKind(
                        user_name=user['user_name'],
                        kind=p_kind
                    )
                )
                add_recommend_set = News.objects.filter(kind=p_kind).order_by('-hot_rate')[:20]
                add_recommend.extend(
                    [UserToRecommendUrl(
                        url=news.url,
                        user_name=user['user_name']
                    ) for news in add_recommend_set]
                )
            Member.objects.create(
                nick_name=user['nick_name'],
                user_name=user['user_name'],
                password=user['password']
            )
            UserToKind.objects.bulk_create(add_kind)
            UserToRecommendUrl.objects.bulk_create(add_recommend)
            result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def sign_in(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }

    try:
        user = json.loads(request.body)
        re_flag = True
        for i in xrange(1, len(user_item)):
            if not re.match(pattern_user_dict[user_item[i]], user[user_item[i]]):
                re_flag = False
                result['retcode'] = 10003
                result['error_msg'] = 'error in %s' % user_item[i]
                break
        
        if re_flag:
            try:
                member = Member.objects.get(user_name=user['user_name'])
                if member.password == user['password']:
                    result['retcode'] = 0
                    if not request.session.exists('user_name'):
                        request.session['user_name'] = member.user_name
                    request.session.set_expiry(604800)
                    result['nick_name'] = member.nick_name
                    response = HttpResponse(json.dumps(result), content_type='application/json')
                    return response
                else:
                    result['retcode'] = 403
                    result['error_msg'] = 'illegal password'
            except:
                result['retcode'] = 10001
                result['error_msg'] = 'user not found'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def sign_out(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }

    try:
        if not check_user_cookie(request):
            result['retcode'] = 403
            result['error_msg'] = 'illegal cookies'
            return HttpResponse(json.dumps(result), content_type='application/json')
        try:
            result['retcode'] = 0
            request.session.flush()
            response = HttpResponse(json.dumps(result), content_type='application/json')
            return response
        except:
            result['retcode'] = 10001
            result['error_msg'] = 'session not found'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def change_tags(request):
    result = {
        'retcode': 10000,
        'error_msg': '',
    }
    
    try:
        if not check_user_cookie(request):
            result['retcode'] = 403
            result['error_msg'] = 'illegal cookies'
            return HttpResponse(json.dumps(result), content_type='application/json')
        all_data = json.loads(request.body)
        p_user_name = request.session.get('user_name')
        print p_user_name
        print all_data['change_tags'].encode('utf-8')
        if p_user_name:
            change_kind_set = set(all_data['change_tags'].split('/'))
            change_kind_set = kind_item_set & change_kind_set
            if change_kind_set:
                p_kinds = list(UserToKind.objects.filter(user_name=p_user_name).values_list('kind', flat=True))
                p_kinds_set = set(p_kinds)
                add_kind_list = list(change_kind_set - p_kinds_set)
                delete_kind_list = list(p_kinds_set - change_kind_set)
                print 'us tag'
                print add_kind_list
                print delete_kind_list
                if add_kind_list:
                    add_kind = []
                    add_recommend = []
                    for p_kind in add_kind_list:
                        add_kind.append(
                            UserToKind(
                                user_name=p_user_name,
                                kind=p_kind
                            )
                        )
                        add_recommend_set = News.objects.filter(kind=p_kind).order_by('-hot_rate')[:20]
                        add_recommend.extend(
                            [UserToRecommendUrl(
                                url=news.url,
                                user_name=p_user_name
                            ) for news in add_recommend_set]
                        )
                    UserToKind.objects.bulk_create(add_kind)
                    UserToRecommendUrl.objects.bulk_create(add_recommend)
                if delete_kind_list:
                    delete_url_list = list(News.objects.filter(kind__in=delete_kind_list).values_list('url', flat=True))
                    UserToKind.objects.filter(kind__in=delete_kind_list, user_name=p_user_name).delete()
                    UserToRecommendUrl.objects.filter(user_name=p_user_name, url__in=delete_url_list).delete()
                result['retcode'] = 0
            else:
                result['retcode'] = 10003
                result['error_msg'] = 'illegal tags'
        else:
            result['retcode'] = 10001
            result['error_msg'] = 'user not found'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')
