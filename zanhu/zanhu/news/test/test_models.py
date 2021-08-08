#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from test_plus.test import TestCase
from zanhu.news.models import News

class TestNews(TestCase):
    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.first_news = News.objects.create(user=self.user,content="first news")
        self.second_news = News.objects.create(user=self.user,content="second news")
        self.third_news = News.objects.create(user=self.other_user,
                                              content="comment for first news",
                                              reply=True,
                                              parent=self.first_news)

    def test_switch_liked(self):
        self.first_news.switch_liked(self.user)
        assert self.first_news.count_likes() == 1
        assert self.user in self.first_news.get_likes()

    def test_reply_this(self):
        init_count = News.objects.count()
        self.first_news.reply_this(self.other_user, "first comment for news")
        assert News.objects.count() == init_count + 1
        assert self.first_news.comment_count() == 2
        assert self.third_news in self.first_news.get_thread()

    def test__str__(self):
        self.assertEqual(self.first_news.__str__(), "first news")

