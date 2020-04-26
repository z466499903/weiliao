# -*- coding: utf-8 -*-
# @Time: 2020/4/26 10:53
# @Author: ZhangRui
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication, \
    get_authorization_header
from rest_framework import exceptions

from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async

WLUser = get_user_model()
def generate_jwt(user):
    # 过期时间
    timestamp = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')
    # 因为jwt.encode返回的bytes数据，因此需要decode解码str类型
    token = jwt.encode({"userid": user.pk, 'exp': timestamp},
                       settings.SECRET_KEY).decode('utf-8')
    return token


class JWTAuthentication(BaseAuthentication):
    """
        Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Authorization 不可用！'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Authorization 不可用！应该提供一个空格！'
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY)
            userid = jwt_info.get("userid")
            try:
                user = WLUser.objects.get(pk=userid)
                return (user, jwt_token)
            except:
                msg = "用户不存在"
                raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = 'Token已经过期了！'
            raise exceptions.AuthenticationFailed(msg)


@database_sync_to_async
def get_user(scope):
    """
    用来获取用户
    """
    user = None
    query_string = scope['query_string']
    jwt_token = query_string.decode()
    try:
        jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY)
    except jwt.ExpiredSignatureError:
        msg = 'Token已经过期了！'
        raise exceptions.AuthenticationFailed(msg)
    userid = jwt_info.get("userid")
    try:
        user = WLUser.objects.get(pk=userid)
    except ObjectDoesNotExist:
        msg = "用户不存在"
        raise exceptions.AuthenticationFailed(msg)
    return user


class TokenAuthMiddleware(BaseMiddleware):
    keyword = 'JWT'
    model = None

    def __call__(self, scope):
        try:
            rst = super().__call__(scope)
        except exceptions.AuthenticationFailed:
            return WebsocketDenier(scope)
        return rst

    def populate_scope(self, scope):
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope)


# 将TokenAuthMiddlewareStack变成一个装饰器
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(inner)