# -*- coding:utf-8 -*-
from django.conf.urls import url
from cases.models import Post
from . import views
# 下面的是rest framwork 的路由
from django.conf.urls import url, include
from rest_framework import routers
from cases import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'cases'  # 告诉 django 这个 urls.py 模块是属于 blog 应用的

# 下面的是rest framwork 的路由
router = routers.DefaultRouter()
router.register(r'post_list', views.PostViewSet)
# router.register(r'post_list/(?P<fact>[0-9]+)/$',views.PostViewSet)

urlpatterns = [

    url(r'^post_by_page/$', views.getPostListByPage),  # 分页
    url(r'^save_post/$', views.save_post),  # # 增加新的post的接口
    url(r'^update_post/$', views.update_post),  # 更新update_post
    url(r'^post_by_worker/$', views.getPostListByWorker),  # 根据管家获得上传的post列表
    url(r'^photos_in_post/$', views.getPhotosByPost),  # 根据管家获得上传的post列表
    url(r'^delete_photo/$', views.delete_photo),  # 根据管家获得上传的post列表
    url(r'^login_worker/$', views.login_worker),  # 管家登录
    url(r'^new_password_worker/$', views.new_password_worker),  # 管家登录new_password_worker
    url(r'^get_services/$', views.get_services),  # 获得服务项目列表

    url(r'^post_by_page/$', views.getPostListByVillage),  # 条件查询的方法2
    url(r'^post_by_district/(?P<district>[0-9]+)/$', views.getPostListByBistrict),  # 条件查询的方法1

    # 下面的是rest framwork 的路由
    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
