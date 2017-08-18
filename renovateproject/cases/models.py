# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Service(models.Model):
    # 服务名称
    name = models.CharField(max_length=70, blank=True)
    # 费用标准,如5元/m2
    price = models.PositiveIntegerField(default=0, blank=True)
    # 描述,如 适用于墙面有轻微裂缝等等
    describe = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Scheme(models.Model):
    # 房间,如主卧\厨房\卫生间\整体
    room = models.CharField(max_length=70, blank=True)
    # 有损坏的部位描述
    damage_des = models.CharField(max_length=70, blank=True)
    # 损坏处理措施
    measures = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.room


class Worker(models.Model):
    # 姓名
    name = models.CharField(max_length=70, blank=True)
    # 手机号
    tele = models.CharField(max_length=70, blank=True)
    # 初始密码
    password = models.CharField(max_length=70, blank=True, default='111')
    # 案例个数
    num = models.PositiveIntegerField(default=0, blank=True)  # 字段的类型为 PositiveIntegerField，该类型的值只允许为正整数或 0
    # 好评度
    praise = models.CharField(max_length=70, blank=True)

    def get_worker_cases_url(self):
        return reverse('cases:worker-cases-url', kwargs={'worker_pk': self.pk})

    def __str__(self):
        return self.name


class ProtectionImage(models.Model):
    des = models.CharField(max_length=70, blank=True)
    path = models.FileField(upload_to='./cases/static/imgs/', blank=True)

    def __str__(self):
        return self.des


class WorkSiteImage(models.Model):
    des = models.CharField(max_length=70, blank=True)
    path = models.FileField(upload_to='./cases/static/imgs/', blank=True)

    def __str__(self):
        return self.des


class FinishImage(models.Model):
    des = models.CharField(max_length=70, blank=True)
    path = models.FileField(upload_to='./cases/static/imgs/', blank=True)

    def __str__(self):
        return self.des


class Post(models.Model):
    post_imag = models.FileField(upload_to='media/imgs/', blank=True)
    # 小区名称
    village = models.CharField(max_length=70, blank=True)
    DISTRICT_CHOICES = (
        ("01", '朝阳区'),
        ("02", '通州区'),
        ("03", '海淀区'),
        ("04", '东城区'),
        ("05", '西城区'),
        ("06", '丰台区'),
    )
    # todo 位置区域,如北京朝阳(后续可以单独做个表,来管理城市区域)
    district = models.CharField(max_length=70, blank=True, choices=DISTRICT_CHOICES)

    # 预计工期
    predict = models.CharField(max_length=70, blank=True)
    # 实际工期
    fact = models.CharField(max_length=70, blank=True)
    # 开工日期
    created_time = models.DateTimeField(null=True, blank=True)

    # 服务项目,如轻微损坏的墙面刷新
    service = models.ForeignKey(Service, null=True, blank=True)
    # 施工方案,如主卧室的基础性刷新
    scheme = models.ForeignKey(Scheme, null=True, blank=True)
    # 施工管家
    worker = models.ForeignKey(Worker, null=True, blank=True)
    STATE_CHOICES = (
        ("01", '施工中'),
        ("02", '已完工'),
    )
    # 状态,未开工\进行中\已完工
    state = models.CharField(max_length=70, blank=True, choices=STATE_CHOICES, default="01")
    # ss = models.ri
    area = models.CharField(max_length=70, blank=True)

    owner = models.ForeignKey('comments.Owner', blank=True, null=True)

    def __str__(self):
        # python_2_unicode_compatible 装饰器用于兼容 Python2
        return self.village

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('cases:detail-url', kwargs={'pk': self.pk})  # 参数1,指定了返回的路由为,blog应用下的名字为detail-url的路由

    class Meta:
        ordering = ['-created_time']


class StartInImage(models.Model):
    des = models.CharField(max_length=70, blank=True, default="photo")
    path = models.FileField(upload_to='media/imgs/', blank=True)  # todo 其实是一个Filed对象
    post = models.ForeignKey(Post, null=True, blank=True)

    def __str__(self):
        return self.des


class ProtectionImage(models.Model):
    des = models.CharField(max_length=70, blank=True, default="photo")
    path = models.FileField(upload_to='media/imgs/', blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)

    def __str__(self):
        return self.des


class WorkSiteImage(models.Model):
    des = models.CharField(max_length=70, blank=True, default="photo")
    path = models.FileField(upload_to='media/imgs/', blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)

    def __str__(self):
        return self.des


class FinishImage(models.Model):
    des = models.CharField(max_length=70, blank=True, default="photo")
    path = models.FileField(upload_to='media/imgs/', blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)

    def __str__(self):
        return self.des
