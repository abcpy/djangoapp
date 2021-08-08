#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from zanhu.helpers import ajax_required, AuthorRequireMixin
from django.urls import reverse_lazy
from django.http import JsonResponse

from zanhu.news.models import News


class NewsListView(LoginRequiredMixin,  ListView):
    model = News
    template_name = "news/news_list.html"

    def get_queryset(self):
        return News.objects.filter(reply=False)


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news:list")

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_new(request):
    """
    发送动态， AJAX POST请求
    :param request:
    :return:
    """
    post = request.POST["post"].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html',{"news":posted,"request":request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """
    点赞或取消点赞
    :param request:
    :return:
    """
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    news.switch_liked(request.user)
    # print(news.count_likes()) 1
    return JsonResponse({"likes": news.count_likes()})

@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    # print(news.get_thread()) <QuerySet [<News: 8888>]>
    news_html = render_to_string("news/news_single.html", {"news":news})
    thread_html = render_to_string("news/news_thread.html", {"thread":news.get_thread()})
    return JsonResponse({
        "uuid":news_id,
        "news":news_html,
        "thread": thread_html
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
   data = request.POST['reply'].strip()
   parent_id = request.POST['parent']
   parent = News.objects.get(pk=parent_id)
   if data:
       parent.reply_this(request.user, data)
       return JsonResponse({'comments': parent.comment_count()})
   else:
       return HttpResponseBadRequest("内容不能为空")






