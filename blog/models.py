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
