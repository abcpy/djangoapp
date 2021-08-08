from django.urls import path

from zanhu.news.views import NewsListView, NewsDeleteView
from zanhu.news.views import post_new,like, get_thread, post_comment

app_name = "news"
urlpatterns = [
    path("", view=NewsListView.as_view(), name="list"),
    path("post-news/", view=post_new, name="post_news"),
    path("delete/<str:pk>", view=NewsDeleteView.as_view(), name="delete_news"),
    path("like/", view=like, name="like_news"),
    path("get-thread/", view=get_thread, name="get_thread"),
    path("post-comment/", view=post_comment, name="post_comment"),
]
