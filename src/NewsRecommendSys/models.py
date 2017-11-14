# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserToTags(models.Model):
    """
    从addUserTags返回值获得
    一天更新一次，需要五天浏览过的标题
    每次更新都要清空表中数据并写入新数据
    """
    tag = models.CharField(max_length=50)
    user_name = models.CharField(max_length=14)
    weight = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.tag
    
    def to_dict(self):
        return {
            'tag': self.tag,
            'user_name': self.user_name,
            'weight': self.weight,
        }


class UserToReadUrl(models.Model):
    """
    用户看过的新闻的链接
    实时添加
    记录随新闻总数据库每天同步清理
    """
    url = models.CharField(max_length=200)
    user_name = models.CharField(max_length=14)
    
    def __unicode__(self):
        return self.url
    
    def to_dict(self):
        return {
            'url': self.url,
            'user_name': self.user_name,
        }


class UserToDateTitle(models.Model):
    """
    用户每天点击过的新闻的标题表
    实时添加
    每天更新都要清除超过5天的记录
    """
    title = models.CharField(max_length=100)
    user_name = models.CharField(max_length=14)
    date = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.title
    
    def to_dict(self):
        return {
            'title': self.title,
            'user_name': self.user_name,
            'date': self.date,
        }


class UserToRecommendUrl(models.Model):
    """
    用户的每天推荐新闻链接表
    三小时更新一次
    每次更新都要清空表中数据并写入新数据
    """
    url = models.CharField(max_length=200)
    user_name = models.CharField(max_length=14)
    
    def __unicode__(self):
        return self.url
    
    def to_dict(self):
        return {
            'url': self.url,
            'user_name': self.user_name,
        }
