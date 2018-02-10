#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/$', views.article_detail, name='full'),
    url(r'^login/$', login, {'template_name': 'blog/login.html'},
        name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^reg/$', views.RegisterView.as_view(), name='reg'),
    url(r'^access_error_to_post/$', views.access_error_to_post),
    url(r'^access_error_to_modify/$', views.access_error_to_modify),
    url(r'^edit/$', views.EditView.as_view(), name='edit'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditPostView.as_view(),
        name='editpost'),
    url(r'^edit/delete/(?P<pk>[0-9]+)/$', views.delete_article, name='delete'),
    url(r'^edit/newpost/$', views.NewPostView.as_view(), name='newpost'),
    url(r'^error_expired/$', views.error_expired),
    url(r'^success_register_account/$',
        views.success_register_account),
    url(r'^success_activated_account/$',
        views.success_activated_account),
    url(r'^confim/(?P<activation_key>[a-zA-Z0-9_]+)/$', views.confirm_registration),
    url(r'^repeat_email/$', views.RepeatEmailView.as_view(), name='repeat'),
]
