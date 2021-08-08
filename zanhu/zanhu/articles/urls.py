from django.urls import path

from zanhu.articles.views import ArticlesListView, ArticleCreateView, \
    DraftListView, ArticleDetailView, ArticleEditView


app_name = "articles"
urlpatterns = [
    path("", view=ArticlesListView.as_view(), name="list"),
    path("write-new-article/", view=ArticleCreateView.as_view(), name="write_new"),
    path("drafts/", view=DraftListView.as_view(), name="drafts"),
    path("<str:slug>/", view=ArticleDetailView.as_view(), name="article"),
    path("edits/<int:pk>/", view=ArticleEditView.as_view(), name="edit_article"),

]
