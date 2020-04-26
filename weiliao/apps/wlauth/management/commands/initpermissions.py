# -*- coding: utf-8 -*-
# @Time: 2020/4/25 14:40
# @Author: ZhangRui

from django.core.management.base import BaseCommand
from apps.WLhelper.urls import get_all_urlpattern_set
from apps.wlauth.models import WLPermissions

class Command(BaseCommand):

    def save_permissions(self, url_set):
        '''
        保存权限，每个url 保存3条数据
        :param url_set: 一个集合
        :return: 保存成功返回的对象
        '''
        permissions = []
        for item in url_set:
            url_name = item.url_name
            namespace = item.namespace
            for describe in [x[0] for x in WLPermissions.DESCRIBES]:
                permission = WLPermissions(url_name=url_name,
                                           namespace=namespace,
                                           describe=describe)
                permissions.append(permission)
        WLPermissions.objects.all().delete()
        return WLPermissions.objects.bulk_create(permissions)

    def handle(self, *args, **options):
        '''
        生成权限信息
        :param args:
        :param options:
        :return:
        '''
        url_set = get_all_urlpattern_set()
        self.stdout.write(self.style.NOTICE(f'共{len(url_set)}个URL。'))
        op = input("生成权限信息将会清空旧的权限信息，是否确认?(y/n)")
        if op.lower() == 'y':
            try:
                objs = self.save_permissions(url_set)
            except Exception as e:
                print(e)
                self.stdout.write(self.style.ERROR(str(e)))
            else:
                self.stdout.write(self.style.SUCCESS(f'成功保存{len(objs)}个权限。'))
        else:
            self.stdout.write(self.style.WARNING('放弃生成权限信息!'))
