#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views, forms
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/$', views.FullView.as_view(), name='full'),
    url(r'^login/$', login, {'template_name': 'blog/login.html',
        'authentication_form': forms.LoginForm}, name='login'),
]
