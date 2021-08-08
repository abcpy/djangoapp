#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jian__'

from functools import wraps
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth import PermissionDenied


def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是AJAX请求")
        return f(request, *args, **kwargs)
    return wrap


class AuthorRequireMixin(View):
    """
    验证是否为当前作者， 用于状态删除，文章编辑
    """
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

