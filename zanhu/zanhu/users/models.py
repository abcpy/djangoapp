#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse



class User(AbstractUser):
    """Default user for zanhu."""
    nickname = models.CharField(null=True, blank=True,max_length=255, verbose_name="昵称")
    job_title = models.CharField(max_length=50, null=True, blank=True, verbose_name="职称")
    introduction = models.TextField(blank=True, null=True, verbose_name="简介")
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="头像")
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name="城市")
    personal_url = models.URLField(max_length=255, null=True, blank=True,verbose_name="个人链接")
    weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name="微博链接")
    zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name="知乎链接")
    github = models.URLField(max_length=255, null=True, blank=True, verbose_name="github链接")
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name="linked链接")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username
