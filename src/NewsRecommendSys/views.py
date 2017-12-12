# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import os
import json
import re
import time
import traceback

from NewsDB.models import News
from UserDB.views import check_user_cookie
from UserDB.models import *
from NewsRecommendSys.models import *

# 路径准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'temp')

# 数据准备


# 功能函数


# 响应函数
def user_recommend(request):
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
        if p_user_name:
            user_recommend_set = UserToRecommendUrl.objects.filter(user_name=p_user_name)
            recommend_url_list = list(user_recommend_set.values_list('url', flat=True))
            news_set = News.objects.filter(url__in=recommend_url_list)
            result['news'] = [news.to_dict() for news in news_set]
            result['retcode'] = 0
        else:
            result['retcode'] = 10001
            result['error_msg'] = 'user not found'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')


def record(request):
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
        p_url = all_data['url']
        p_title = all_data['title']
        p_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if p_user_name:
            check_news_set = News.objects.filter(url=p_url)
            if check_news_set.exists():
                check_read_url = UserToReadUrl.objects.filter(url=p_url, user_name=p_user_name)
                if not check_read_url.exists():
                    UserToReadUrl.objects.create(
                        url=p_url,
                        user_name=p_user_name
                    )
                check_date_title = UserToDateTitle.objects.filter(title=p_title, user_name=p_user_name, date=p_date)
                if not check_date_title.exists():
                    UserToDateTitle.objects.create(
                        title=p_title,
                        user_name=p_user_name,
                        date=p_date
                    )
                result['retcode'] = 0
            else:
                result['retcode'] = 10002
                result['error_msg'] = 'news not found'
        else:
            result['retcode'] = 10001
            result['error_msg'] = 'user not found'
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
        result['error_msg'] = traceback.format_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')
