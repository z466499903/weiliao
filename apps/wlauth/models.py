# -*- coding: utf-8 -*-
# @Time: 2020/4/24 15:53
# @Author: ZhangRui
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from shortuuidfield import ShortUUIDField


class WLUserManage(BaseUserManager):

    def _create_user(self, nickname, password, email, telephone,
                     **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not nickname:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        nickname = self.model.normalize_username(nickname)
        user = self.model(nickname=nickname, email=email, telephone=telephone,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, nickname, password=None, email=None, telephone=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, password, email, telephone,
                                 **extra_fields)

    def create_superuser(self, nickname, password=None, email=None,
                         telephone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(nickname, password, email, telephone,
                                 **extra_fields)


class WLUser(AbstractBaseUser):
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    nickname = models.CharField(max_length=50,
                                validators=(MinLengthValidator(limit_value=1),),
                                null=False, blank=False, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱', unique=True, null=False,
                              blank=True)
    telephone = models.CharField(max_length=11, unique=True, null=False,
                                 blank=True,
                                 validators=(RegexValidator(
                                     regex=r'1[35678]\d{9}'),),
                                 verbose_name='手机号')
    doc = models.CharField(max_length=255, null=False, blank=True,
                           verbose_name='个人简介')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')
    is_staff = models.BooleanField(default=False, verbose_name='是否是管理员')
    time_joined = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')
    avatar = models.URLField(null=False, blank=True, verbose_name='头像')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email', 'telephone']
    objects = WLUserManage()

    class Meta:
        db_table = 'wluser'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname


class WLPermissions(models.Model):
    READ_PERMISSION = 1
    WRITE_PERMISSION = 2
    UPDATE_PERMISSION = 3

    describes = (
        (READ_PERMISSION, 'read'),
        (WRITE_PERMISSION, 'write'),
        (UPDATE_PERMISSION, 'update')
    )

    path = models.CharField(max_length=100, unique=True, null=False,
                            blank=False, verbose_name='路由')
    describe = models.SmallIntegerField(choices=describes, verbose_name='权限描述',
                                        null=False, blank=False)
    users = models.ManyToManyField(WLUser, related_name='permissions',
                                   verbose_name='关联用户')

    class Meta:
        db_table = 'wlpermissions'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class WLGroup(models.Model):
    group_name = models.CharField(max_length=50, unique=True, null=False,
                                  blank=False, verbose_name='分组名')
    permissions = models.ManyToManyField(WLPermissions, related_name='groups',
                                         verbose_name='关联权限')
    users = models.ManyToManyField(WLUser, related_name='groups',
                                   verbose_name='关联用户')
