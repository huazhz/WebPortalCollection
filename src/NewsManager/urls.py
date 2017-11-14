"""NewsManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin

# from django.views import static
import NewsDB.views
import UserDB.views
import NewsRecommendSys.views

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    
    # static url
    
    # data url
    url(r'^insert_news/$', NewsDB.views.insert_news, name='insert_news'),
    url(r'^all_news/$', NewsDB.views.all_news, name='all_news'),
    url(r'^news/$', NewsDB.views.news, name='news'),
    url(r'^query/$', NewsDB.views.query, name='query'),
    # url(r'^clean_news/$', NewsDB.views.clean_news, name='clean_news'),

    # user url
    url(r'^sign_up/$', UserDB.views.sign_up, name='sign_up'),
    url(r'^sign_in/$', UserDB.views.sign_in, name='sign_in'),
    url(r'^sign_out/$', UserDB.views.sign_out, name='sign_out'),
    url(r'^change_tags/$', UserDB.views.change_tags, name='change_tags'),

    # recommend url
    url(r'^recommend/$', NewsRecommendSys.views.user_recommend, name='recommend'),
    url(r'^record/$', NewsRecommendSys.views.record, name='record'),
]
