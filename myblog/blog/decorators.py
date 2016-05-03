#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url=None, a=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function and a:
        return actual_decorator(function)
    return actual_decorator





















'''
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.conf import settings
from django.shortcuts import redirect
def check_decorator(view=None,
                    condition_func = lambda request, *args, **kwargs: True,
                    false_func = lambda request, *args, **kwargs: HttpResponse()):

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            login_url = '/login'
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            if not condition_func(request, *args, **kwargs):
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(path, resolved_login_url, redirect_field_name)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator(view) if view else decorator


def access_private_post(view=None, redirect_url='/login/'):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            login_url = '/login'
            if not view:
                return redirect('/login')
            return view(request, *args, **kwargs)
        return wrapper
    return decorator(view)
'''