from django.contrib import admin

# Register your models here.

from .models import Service, Scheme, Worker, Post, StartInImage, ProtectionImage, WorkSiteImage, FinishImage


class StartInImageInline(admin.StackedInline):
    model = StartInImage
    extra = 0


class ProtectionImageInline(admin.StackedInline):
    model = ProtectionImage
    extra = 0


class WorkerSiteImageInline(admin.StackedInline):
    model = WorkSiteImage
    extra = 0


class FinishImageInline(admin.StackedInline):
    model = FinishImage
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'village', 'district', 'created_time', 'service', 'worker', 'state']

    def state(self, obj):
        return 'fffff'

    inlines = [StartInImageInline, ProtectionImageInline, WorkerSiteImageInline, FinishImageInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'describe']


class ServiceInline(admin.StackedInline):
    model = Service

    def state(self, obj):
        return 'fffff'

    extra = 0


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    inlines = [ServiceInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Scheme)
admin.site.register(Worker, WorkerAdmin)
# admin.site.register(StartInImage)
# admin.site.register(ProtectionImage)
# admin.site.register(WorkSiteImage)
# admin.site.register(FinishImage)
