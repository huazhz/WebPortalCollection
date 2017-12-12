# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class News(models.Model):
    """
    新闻总数据库
    每天更新清除掉入库超过三天的新闻
    """
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, primary_key=True)
    kind = models.CharField(max_length=50)
    hot_rate = models.FloatField()
    date = models.CharField(max_length=10)
    img_url = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.url
    
    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'kind': self.kind,
            'hot_rate': self.hot_rate,
            'date': self.date,
            'img_url': self.img_url
        }

    
class NewsToLimitTags(models.Model):
    """
    新闻对应最多四个标签
    每次爬虫加入数据时添加
    每天随新闻总表清除
    """
    tag = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.tag
    
    def to_dict(self):
        return {
            'tag': self.tag,
            'url': self.url,
        }


class NewsToTags(models.Model):
    """
    新闻对应所有分词标签
    每次爬虫加入数据时添加
    每天随新闻总表清除
    """
    tag = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.tag
    
    def to_dict(self):
        return {
            'tag': self.tag,
            'url': self.url,
        }
