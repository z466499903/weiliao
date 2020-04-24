# -*- coding: utf-8 -*-
# @Time: 2020/4/23 19:31
# @Author: ZhangRui


from django.urls import path
from .view import index
app_name = 'wlauth'
urlpatterns = [
    path('', index,name='index'),
]