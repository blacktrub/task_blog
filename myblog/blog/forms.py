#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password', max_length=30)
