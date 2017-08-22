from django.db import models

# Create your models here.
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Order(models.Model):
    STATE_CHOICES = (
        ("01", '已下单'),
        ("02", '已取消'),
        ("03", '已完成'),
    )
    order_num = models.CharField(max_length=70, blank=True)
    # 施工管家
    worker = models.ForeignKey('cases.Worker', null=True, blank=True)
    owner = models.ForeignKey('comments.Owner', blank=True, null=True)
    service = models.ForeignKey('cases.Service', null=True, blank=True)
    schemeInService = models.ForeignKey('cases.SchemeInService', null=True, blank=True)
    state = models.CharField(max_length=70, blank=True, choices=STATE_CHOICES, default="01")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_num
