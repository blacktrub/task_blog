#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import datetime
import random
from django.core.mail import send_mail
from .models import UserProfile


def email_autentification(user, auth=False):
    activation_key = hashlib.sha1(str(random.random()).encode()+user.email.encode()).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    if not auth:
        user_profile = UserProfile(user=user, activation_key=activation_key,
                                   key_expires=key_expires)
        user_profile.save()
        email_subject = 'Подтверждение регистрации'
        email_body = '''Привет %s, спасибо за регистрацию! Осталось всего чуть-чуть,
        перейди по ссылке:
        http://127.0.0.1:8000/confim/%s''' % (user.username, activation_key)
    else:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.activation_key = activation_key
        user_profile.key_expires = key_expires
        user_profile.save()
        email_subject = 'Повторное подтверждение'
        email_body = '''Привет %s, вы повторно запросили авторизацию, перейдите по ссылке
        http://127.0.0.1:8000/confim/%s''' % (user.username, activation_key)

    send_mail(email_subject, email_body, 'blogdarkpy@gmail.com',
              [user.email], fail_silently=False)
    return 1
