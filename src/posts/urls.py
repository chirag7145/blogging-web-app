from django.conf.urls import url,include
from django.contrib import admin
from .import views

urlpatterns = [
    url(r'^$',"posts.views.post_list",name='list'),
    # url(r'^(?P<slug>[\w-]+)/$',"posts.views.post_detail",name='detail'),
    # url(r'^(?P<id>\d+)/$',"posts.views.post_detail",name='detail'),
    url(r'^create/$',"posts.views.post_create",name='create'),
#     url(r'^(?P<id>\d+)/edit/$',"posts.views.post_update",name='update'),
#     url(r'^(?P<id>\d+)/delete/$',"posts.views.post_delete",name='delete'),
#

    url(r'^(?P<slug>[\w-]+)/$', "posts.views.post_detail", name='detail'), #Django Code Review #3 on joincfe.com/youtube/
    url(r'^(?P<slug>[\w-]+)/edit/$', "posts.views.post_update", name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', "posts.views.post_delete"),
]
