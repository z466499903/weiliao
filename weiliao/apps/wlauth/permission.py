# -*- coding: utf-8 -*-
# @Time: 2020/4/26 9:20
# @Author: ZhangRui
from rest_framework.permissions import BasePermission
from apps.wlauth.models import WLPermissions


class URLBasePermission(BasePermission):
    '''
        视图权限，默认为写权限
    '''
    describe = WLPermissions.WRITE_PERMISSION
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            return request.user.has_permissions(request, self.describe)
        else:
            return False


class URLWritePermission(URLBasePermission):
    '''
        读权限
    '''
    describe = WLPermissions.WRITE_PERMISSION
    pass


class URLReadPermission(URLBasePermission):
    '''
         更新权限
    '''
    describe = WLPermissions.READ_PERMISSION
    pass


class URLUpdatePermission(URLBasePermission):
    describe = WLPermissions.UPDATE_PERMISSION
    pass
