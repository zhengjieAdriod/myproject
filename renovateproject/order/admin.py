from django.contrib import admin

# Register your models here.
from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk']


admin.site.register(Order,OrderAdmin)
