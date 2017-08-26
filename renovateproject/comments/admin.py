from django.contrib import admin

# Register your models here.

from .models import Comment, Owner


# Register your models here.
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'telephone', 'password']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Owner, OwnerAdmin)
