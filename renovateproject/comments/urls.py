# -*- coding:utf-8 -*-
# 下面的是rest framwork 的路由
from django.conf.urls import url, include
from rest_framework import routers
from comments import views

app_name = 'comments'  # 告诉 django 这个 urls.py 模块是属于 blog 应用的

# 下面的是rest framwork 的路由
router = routers.DefaultRouter()
urlpatterns = [
    url(r'^comments_by_post/$', views.getCommentsInPost),  # 查询评论
    url(r'^add_comment/$', views.add_comment),  # 新增评论
    url(r'^add_call_back/$', views.add_call_back),  # 回复评论
    url(r'^owner_login/$', views.owner_login),  # 业主登录


    # 下面的是rest framwork 的路由
    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
