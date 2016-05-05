#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/$', views.FullView, name='full'),
    url(r'^login/$', login, {'template_name': 'blog/login.html'},
        name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^reg/$', views.RegisterView.as_view(), name='reg'),
    url(r'^access_error_to_post/$', views.Access_error_to_post),
    url(r'^edit/$', views.EditView.as_view(), name='edit'),
    url(r'^edit/delete/(?P<pk>[0-9]+)/$', views.DeletePost, name='delete'),
]
