from django import forms
from .models import Post, Comment, SummerNote, HashTag
from django_summernote import fields as summer_fields


class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '포스트 제목을 입력하세요'}), required=True)
    content = summer_fields.SummernoteTextFormField(label='', required=True)
    hash_tag = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '태그를 입력하세요  ex) #태그'}),
                               required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'hash_tag')


class SummerForm(forms.ModelForm):
    fields = summer_fields.SummernoteTextFormField(error_messages={'required': (u'데이터를 입력해주세요'), })

    class Meta:
        model = SummerNote
        fields = ('fields',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')
