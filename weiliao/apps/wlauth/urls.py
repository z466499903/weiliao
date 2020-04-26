# -*- coding: utf-8 -*-
# @Time: 2020/4/23 19:31
# @Author: ZhangRui

from django.urls import path
from apps.wlauth.view import LoginView

app_name = 'wlauth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
