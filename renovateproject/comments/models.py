from django.db import models
from django.utils.six import python_2_unicode_compatible


# Create your models here.
# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=100)
    # url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('cases.Post')
    call_back = models.TextField(blank=True, null=True)
    # 施工管家
    worker = models.ForeignKey('cases.Worker', null=True, blank=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']


@python_2_unicode_compatible
class Owner(models.Model):
    telephone = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='111')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.telephone[:10]



