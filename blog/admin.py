from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Post, Comment


class PostModelAdmin(SummernoteModelAdmin):
    pass


admin.site.register(Post)
admin.site.register(Comment)
