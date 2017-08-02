from django.contrib import admin

# Register your models here.

from .models import Comment, Owner
# Register your models here.
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'telephone', 'password']
admin.site.register(Comment)
admin.site.register(Owner, OwnerAdmin)

