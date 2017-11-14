# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Member(models.Model):
    """
    用户总表
    储存用户的全部信息
    """
    nick_name = models.CharField(max_length=14)
    user_name = models.CharField(max_length=14, primary_key=True)
    password = models.CharField(max_length=14)
    
    # more
    
    def __unicode__(self):
        return self.user_name
    
    def to_dict(self):
        return {
            'nick_name': self.nick_name,
            'user_name': self.user_name,
            'password': self.password,
        }


class UserToKind(models.Model):
    """
    用户
    """
    user_name = models.CharField(max_length=14)
    kind = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user_name

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'kind': self.kind,
        }
