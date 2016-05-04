#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps
from django.shortcuts import redirect


def access_private_post(function=None, url=None, access=None):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if not access and not request.user.is_authenticated():
                return redirect(url)
            else:
                return function(request, *args, **kwargs)
        return wrapper
    return decorator
