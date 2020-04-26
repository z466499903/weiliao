# -*- coding: utf-8 -*-
# @Time: 2020/4/26 16:23
# @Author: ZhangRui

from rest_framework import serializers

from apps.wlauth.models import WLUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class UserPartSerializer(serializers.ModelSerializer):
    time_joined = serializers.DateTimeField(format='%Y年%m月%d日')

    class Meta:
        model = WLUser
        exclude = ('password', 'is_staff', 'is_superuser')
