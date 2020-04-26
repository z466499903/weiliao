# -*- coding: utf-8 -*-
# @Time: 2020/4/23 19:31
# @Author: ZhangRui

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.WLhelper.authentications import generate_jwt
from apps.wlauth.models import WLUser
from apps.wlauth.serializers import LoginSerializer, UserPartSerializer

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            if '@' in username:
                user = get_object_or_404(WLUser, email=username)
            else:
                user = get_object_or_404(WLUser, telephone=username)
            if user.check_password(password):
                jwt_token = generate_jwt(user)
                user_serializer = UserPartSerializer(instance=user)
                data = {"jwt_token":jwt_token}
                data.update(user_serializer.data)
                return Response(data)
            else:
                return Response({'message': '密码错误！'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
