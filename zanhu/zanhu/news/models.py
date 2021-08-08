#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from django.db import models
import uuid
from django.conf import settings

# Create your models here.


class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name="publisher", verbose_name="用户")
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name="thread", verbose_name="自关联")
    content = models.TextField(verbose_name="动态内容")
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="liked_news", verbose_name="点赞用户")
    reply = models.BooleanField(default=False, verbose_name="是否为评论")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "首页"
        verbose_name_plural = verbose_name
        ordering = ["-create_at"]

    def __str__(self):
        return self.content

    def switch_liked(self, user):
        """
        点赞或取消点赞
        :param user:
        :return:
        """
        if user in self.liked.all():
            # print(self.liked.all()) <QuerySet [<User: test1>]>
            self.liked.remove(user)
        else:
            self.liked.add(user)

    def get_parent(self):
        """
        返回自关联中的上级记录或者本身
        :return:
        """
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        """
        回复首页的动态
        :param user: 登录的用户
        :param text: 回复的内容
        :return:
        """
        parent = self.get_parent()
        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )

    def get_thread(self):
        """
        反向追溯
        :return:
        """
        parent = self.get_parent()
        # print(parent)  test
        return parent.thread.all()

    def comment_count(self):
        return self.get_thread().count()

    def count_likes(self):
        """
        点赞数
        :return:
        """
        return self.liked.count()

    def get_likes(self):
        """
        所有点赞用户
        :return:
        """
        return self.liked.all()


