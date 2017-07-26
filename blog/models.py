import re

from django.db import models

# Create your models here.
from django.utils import timezone
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = summer_fields.SummernoteTextField(default='')
    hash_tag = models.CharField(max_length=200, default='')
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        if self.published_date is None:
            self.published_date = timezone.now()
            redirect_url = 'post_detail'
        else:
            self.published_date = None
            redirect_url = 'post_draft_detail'
        self.save()
        return redirect_url

    def get_hash_tag_list(self):
        return re.findall(r'(#[ㄱ-ㅎ가-힣a-zA-Z0-9]+)', self.hash_tag)

    def view_hash_tag(self):
        hash_tag_list = []
        for tag in re.findall(r'(#[ㄱ-ㅎ가-힣a-zA-Z0-9]+)', self.hash_tag):
            hash_tag_list.append(tag)

        return hash_tag_list

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class HashTag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
