# -*- coding:utf-8 -*-
from rest_framework import serializers
from comments.models import Comment, Owner


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'name', 'telephone', 'text', 'created_time', 'call_back')


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ('pk', 'password', 'telephone',)
