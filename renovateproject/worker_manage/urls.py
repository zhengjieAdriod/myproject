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

    # todo 点击条增加服务按钮, 以及保存首次新增的服务
    url(r'^add_service/(?P<worker_pk>[0-9]+)/$', views.add_service, name='add_service-url'),

    # todo 点击条目的编辑按钮, 以及保存编辑后的服务和服务子项
    url(r'^edit_service/(?P<service_pk>[0-9]+)/$', views.update_edit_service, name='edit_service-url'),

    # todo 在编辑页面点击完成按钮(保存了编辑数据并跳转到前一页)
    url(r'^edit_service_finish/(?P<service_pk>[0-9]+)/$', views.update_edit_service_finish,
        name='edit_service_finish-url'),

    # todo 删除服务子项
    url(r'^delete_item_service/(?P<service_pk>[0-9]+)/(?P<item_pk>[0-9]+)/$', views.delete_item_service,
        name='delete_item_service-url'),

    # todo 删除服务本项
    url(r'^delete_service/(?P<worker_pk>[0-9]+)/(?P<service_pk>[0-9]+)/$', views.delete_service,
        name='delete_service-url'),

    # 下面的是rest framwork 的路由update_edit_service
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
