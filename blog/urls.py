from django.conf.urls import url
from . import views

urlpatterns = [
    # ^ : 문자열이 시작할때
    # $ : 문자열이 끝날때
    # / 경로로 들어왔을 때 views.post_list를 보여주도록 함.
    # name='post_list' 는 URL에 이름을 붙인 것으로 뷰를 식별한다.
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]