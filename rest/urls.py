from django.urls import path
from .views import *
from django.conf.urls import url


urlpatterns = [

    url(r'^signup', CreateUser.as_view()),
    url(r'^login', UserLogin.as_view()),
    url(r'^get_user', Get_all_user.as_view()),
    url(r'^search', Search.as_view()),
    url(r'^forgot_password',SendMail.as_view()),
    url(r'^change_password',UserChangePassword.as_view()),


]