from django.contrib import admin

# Register your models here.

from .models import Service, Scheme, Worker, Post, StartInImage, ProtectionImage, WorkSiteImage, FinishImage


class StartInImageInline(admin.StackedInline):
    model = StartInImage
    extra = 0

class ProtectionImageInline(admin.StackedInline):
    model = ProtectionImage
    extra = 0
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk','village', 'district', 'created_time', 'service', 'worker']
    inlines = [StartInImageInline,ProtectionImageInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'describe']


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


admin.site.register(Post, PostAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Scheme)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(StartInImage)
admin.site.register(ProtectionImage)
admin.site.register(WorkSiteImage)
admin.site.register(FinishImage)
