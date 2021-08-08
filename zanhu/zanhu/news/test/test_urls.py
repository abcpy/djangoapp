from django.urls import resolve, reverse
from test_plus.test import TestCase
from zanhu.news.models import News


class TestNewsUrls(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.first_news = News.objects.create(user=self.user,
                                              content="first news")

    def test_list_reverse(self):
        self.assertEqual(reverse("news:list"),"/")

    def test_list_resolve(self):
        self.assertEqual(resolve("/").view_name, "news:list")

    def test_post_news_reverse(self):
        self.assertEqual(reverse("news:post_news"),"/post-news/")

    def test_post_news_resolve(self):
        self.assertEqual(resolve("/post-news/").view_name, "news:post_news")

    def test_delete_reverse(self):
        self.assertEqual(reverse("news:delete_news", kwargs={"pk":1}), "/delete/1")

    def test_delete_resolve(self):
        self.assertEqual(resolve("/delete/1").view_name, "news:delete_news")

    def test_like_reverse(self):
        self.assertEqual(reverse("news:like_news"), "/like/")

    def test_like_resolve(self):
        self.assertEqual(resolve("/like/").view_name, "news:like_news")

    def test_get_thread_reverse(self):
        self.assertEqual(reverse("news:get_thread"), "/get-thread/")

    def test_get_thread_resolve(self):
        self.assertEqual(resolve("/get-thread/").view_name, "news:get_thread")

    def test_post_comment_reverse(self):
        self.assertEqual(reverse("news:post_comment"), "/post-comment/")

    def test_post_comment_resolve(self):
        self.assertEqual(resolve("/post-comment/").view_name, "news:post_comment")


