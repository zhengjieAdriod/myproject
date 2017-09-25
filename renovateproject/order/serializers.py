# -*- coding:utf-8 -*-
from rest_framework import serializers

from cases.serializers import ServiceSerializer, WorkerSerializer, SchemeInServiceSerializer
from comments.serializers import OwnerSerializer
from order.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    service = ServiceSerializer()  # CategorySerializer类要写在PostSerializer之前.  返回category的json对象
    worker = WorkerSerializer()  # 因为tag 与 Post是多对多的关系
    owner = OwnerSerializer()
    schemeInService = SchemeInServiceSerializer()

    class Meta:
        model = Order
        fields = ('pk', 'order_num', 'worker', 'owner', 'service', 'schemeInService', 'state', 'created_time')
