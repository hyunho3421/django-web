from django import forms
from .models import Post, Comment, SummerNote
from django_summernote import fields as summer_fields


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)


class SummerForm(forms.ModelForm):
    fields = summer_fields.SummernoteTextFormField(error_messages={'required': (u'데이터를 입력해주세요'), })

    class Meta:
        model = SummerNote
        fields = ('fields',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')
