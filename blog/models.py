import re

from django.db import models

# Create your models here.
from django.utils import timezone
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    content = summer_fields.SummernoteTextField(default='')
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

    def save_hash_tag_list(self, hash_tag_list):
        for hash_tag in re.findall(r'(#[ㄱ-ㅎ가-힣a-zA-Z0-9]+)', hash_tag_list):
            get_hash_tag = HashTag.objects.filter(name=hash_tag)
            if get_hash_tag.exists():
                self.hashtag_set.add(get_hash_tag.get())
            else:
                self.hashtag_set.create(name=hash_tag)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class HashTag(models.Model):
    post = models.ManyToManyField('blog.Post')
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    def tag_name(self):
        return self.name.replace('#', '')

    def font_size(self):
        if self.post.count() == 1:
            return 100
        else:
            return (self.post.count() * 10) + 100 if self.post.count() < 20 else 300
