# -*- coding:utf-8 -*-
from rest_framework import serializers
from cases.models import Service, Worker, Post, Scheme, StartInImage, ProtectionImage, WorkSiteImage, FinishImage, \
    SchemeInService


class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Worker
        fields = ('pk', 'name', 'tele', 'num', 'praise',)


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    worker = WorkerSerializer()

    class Meta:
        model = Service
        fields = ('name', 'type', 'price', 'describe', 'scope', 'worker','image',)


class SchemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scheme
        fields = ('room', 'damage_des', 'measures',)


class SchemeInServiceSerializer(serializers.HyperlinkedModelSerializer):
    Service = ServiceSerializer()

    class Meta:
        model = SchemeInService
        fields = ('pk', 'Service', 'image', 'name', 'price', 'describe',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    # category = serializers.ReadOnlyField(source='category.name')#表示category字段的值category的一个属性
    # category = CategorySerializer(many=True, read_only=True)#many=True表示category字段的值为数组
    service = ServiceSerializer()  # CategorySerializer类要写在PostSerializer之前.  返回category的json对象
    worker = WorkerSerializer()  # 因为tag 与 Post是多对多的关系
    scheme = SchemeSerializer()  # 因为tag 与 Post是多对多的关系

    # start_in_image = StartInImageSerializer(many=True)  # 因为tag 与 Post是多对多的关系
    # protection_image = ProtectionImageSerializer(many=True)  # 因为tag 与 Post是多对多的关系
    # work_site_image = WorkSiteImageSerializer(many=True)  # 因为tag 与 Post是多对多的关系
    # finish_image = FinishImageSerializer(many=True)  # 因为tag 与 Post是多对多的关系
    class Meta:
        model = Post
        fields = (
            'pk', 'post_imag', 'village', 'district', 'created_time', 'area', 'predict', 'fact',
            'state', 'service', 'worker', 'scheme')


class StartInImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StartInImage
        fields = ('pk', 'des', 'path')


class ProtectionImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProtectionImage
        fields = ('pk', 'des', 'path')


class WorkSiteImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkSiteImage
        fields = ('pk', 'des', 'path')


class FinishImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinishImage
        fields = ('pk', 'des', 'path')
