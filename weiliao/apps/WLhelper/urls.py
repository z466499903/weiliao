# -*- coding: utf-8 -*-
# @Time: 2020/4/24 19:17
# @Author: ZhangRui

import re
from collections import namedtuple
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from apps.WLhelper.exceptions import URLNameIsEmptyException

UrlNameTuple = namedtuple('UrlNameTuple', ['namespace', 'url_name'])

def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_set):
    """
    递归的去获取URL
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_set: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，讲路由添加到url_ordered_dict
            if not item.name:
                raise URLNameIsEmptyException('URL路由中必须设置name属性')
            url = pre_url + str(item.pattern)
            if not check_url_exclude(url):
                url_set.add(UrlNameTuple(pre_namespace, item.name))
        elif isinstance(item, URLResolver):  # 路由分发，递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + str(item.pattern),
                           item.url_patterns, url_set)


def get_all_urlpattern_set() -> set:
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    url_set = set()

    md = import_string(settings.ROOT_URLCONF)  # from luff.. import urls
    recursion_urls(None, '/', md.urlpatterns, url_set)  # 递归去获取所有的路由

    return url_set
