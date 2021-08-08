#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from test_plus.test import TestCase
from django.test.client import Client
from zanhu.news.models import News
from django.urls import reverse

class TestNewsView(TestCase):
    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user_02")
        self.client = Client()
        self.other_client = Client()

        self.client.login(username="user01", password="password")
        self.other_client.login(username="user_02", password="password")

        self.first_news = News.objects.create(user=self.user, content="first news")
        self.second_news = News.objects.create(user=self.user, content="second news")
        self.third_news = News.objects.create(user=self.other_user,
                                              content="comment for first news",
                                              reply=True,
                                              parent=self.first_news)

    def test_news_list(self):
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200
        assert self.first_news in response.context["news_list"]
        assert self.second_news in response.context["news_list"]
        assert self.third_news not in response.context["news_list"]

    def test_delete_news(self):
        init_count = News.objects.count()
        response = self.client.post(reverse("news:delete_news",  kwargs={"pk":self.second_news.pk}))
        assert response.status_code == 302
        assert News.objects.count() == init_count - 1

    def test_post_news(self):
        init_count = News.objects.count()
        response = self.client.post(reverse("news:post_news"), {"post":"first post"},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert News.objects.count() == init_count + 1

    def test_like(self):
        response = self.client.post(reverse("news:like_news"), {"news":self.first_news.pk},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200

    def test_get_thread(self):
        response = self.client.get(reverse("news:get_thread"), {"news":self.first_news.pk},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["uuid"] == str(self.first_news.pk)
        assert "first news" in response.json()["news"]
        assert "comment for first news" in response.json()["thread"]

    def test_post_comment(self):
        response = self.client.post(reverse("news:post_comment"),
                                    {"reply": "second comment",
                                     "parent": self.second_news.pk},

                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["comments"] == 1








