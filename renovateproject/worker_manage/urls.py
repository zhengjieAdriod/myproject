# -*- coding:utf-8 -*-
# 下面的是rest framwork 的路由
from django.conf.urls import url, include
from rest_framework import routers
from worker_manage import views

app_name = 'worker_manage'  # 告诉 django 这个 urls.py 模块是属于 blog 应用的

# 下面的是rest framwork 的路由
router = routers.DefaultRouter()
urlpatterns = [
    url(r'^form/$', views.index, name='form-url'),
    url(r'^manager/(?P<worker_pk>[0-9]+)/$', views.manager, name='manager-url'),
    url(r'^tab_manage/$', views.tab_manage, name='tab_manage-url'),
    url(r'^edit_service/(?P<service_pk>[0-9]+)/$', views.update_edit_service, name='edit_service-url'),
    url(r'^add_service/(?P<worker_pk>[0-9]+)/$', views.add_service, name='add_service-url'),
    url(r'^post_service_item/(?P<worker_pk>[0-9]+)/(?P<service_pk>[0-9]+)/(?P<form_item_pk>[0-9]+)/$', views.post_service_item,
        name='post_service_item-url'),

    # url(r'^update_edit_service/(?P<service_pk>[0-9]+)/$', views.update_edit_service, name='update_edit_service-url'),
    # 下面的是rest framwork 的路由update_edit_service
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
