from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Service(models.Model):
    # ��������
    name = models.CharField(max_length=70, blank=True)
    # ���ñ�׼,��5Ԫ/m2
    price = models.PositiveIntegerField(default=0, blank=True)
    # ����,�� ������ǽ������΢�ѷ�ȵ�
    describe = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Scheme(models.Model):
    # ����,������\����\������\����
    room = models.CharField(max_length=70, blank=True)
    # ���𻵵Ĳ�λ����
    damage_des = models.CharField(max_length=70, blank=True)
    # �𻵴����ʩ
    measures = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.room


class Worker(models.Model):
    # ����
    name = models.CharField(max_length=70, blank=True)
    # �ֻ���
    tele = models.CharField(max_length=70, blank=True)
    # ��ʼ����
    password = models.CharField(max_length=70, blank=True, default='111')
    # ��������
    num = models.PositiveIntegerField(default=0, blank=True)  # �ֶε�����Ϊ PositiveIntegerField�������͵�ֵֻ����Ϊ�������� 0
    # ������
    praise = models.CharField(max_length=70, blank=True)

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
    # С������
    village = models.CharField(max_length=70, blank=True)
    # λ������,�籱������
    district = models.CharField(max_length=70, blank=True)

    # Ԥ�ƹ���
    predict = models.CharField(max_length=70, blank=True)
    # ʵ�ʹ���
    fact = models.CharField(max_length=70, blank=True)
    # ��������
    created_time = models.DateTimeField(null=True, blank=True)

    # ������Ŀ,����΢�𻵵�ǽ��ˢ��
    service = models.ForeignKey(Service, null=True, blank=True)
    # ʩ������,�������ҵĻ�����ˢ��
    scheme = models.ForeignKey(Scheme, null=True, blank=True)
    # ʩ���ܼ�
    worker = models.ForeignKey(Worker, null=True, blank=True)

    # ״̬,δ����\������\���깤
    state = models.CharField(max_length=70, blank=True)
    area = models.CharField(max_length=70, blank=True)



    def __str__(self):
        # python_2_unicode_compatible װ�������ڼ��� Python2
        return self.village

    # �Զ��� get_absolute_url ����
    def get_absolute_url(self):
        return reverse('cases:detail-url', kwargs={'pk': self.pk})  # ����1,ָ���˷��ص�·��Ϊ,blogӦ���µ�����Ϊdetail-url��·��

    class Meta:
        ordering = ['-created_time']


class StartInImage(models.Model):
    des = models.CharField(max_length=70, blank=True, default="photo")
    path = models.FileField(upload_to='media/imgs/', blank=True)  # todo ��ʵ��һ��Filed����
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
