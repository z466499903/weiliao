# -*- coding: utf-8 -*-
# @Time: 2020/4/23 19:31
# @Author: ZhangRui
from django.shortcuts import HttpResponse
from apps.WLhelper.urls import get_all_url_dict
def index(request):
    url_dict = get_all_url_dict()
    print(url_dict)
    return HttpResponse("success")