# -*- coding:utf-8 -*-
# 下面的是rest framwork 的路由
from django.conf.urls import url, include
from rest_framework import routers
from order import views

app_name = 'order'  # 告诉 django 这个 urls.py 模块是属于 blog 应用的

# 下面的是rest framwork 的路由
router = routers.DefaultRouter()
urlpatterns = [
    url(r'^add_order/$', views.add_order, name='add_order-url'),

    # 下面的是rest framwork 的路由
    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
