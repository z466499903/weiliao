# -*- coding: utf-8 -*-
# @Time: 2020/4/25 18:16
# @Author: ZhangRui
from rest_framework.routers import DefaultRouter


class WLRouter(DefaultRouter):
    '''
        不引入 api-root url
    '''
    include_root_view = False