from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.apiMain, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^get/api/$', views.getApi, name='getApi'),
]