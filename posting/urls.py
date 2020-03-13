from django.urls import path
from .views import *
from django.conf.urls import url


urlpatterns = [


    url(r'^post',Posts.as_view()),
    url(r'^get',Posts.as_view()),
    url(r'^update',Posts.as_view()),
    # url(r'^get_post',Get_Post.as_view()),
    url(r'^update/(?P<id>[0-9]+)$', Posts.as_view()),
    url(r'^user_post',Filter_Post.as_view()),
    url(r'^week',week.as_view()),
    url(r'^comment',Post_Comment.as_view()),
    url(r'^detail',Detail.as_view()),

]