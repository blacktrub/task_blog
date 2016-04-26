#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=50)
    user_access = models.BooleanField(default=False)
    user_active = models.BooleanField(default=False)


class Article(models.Model):
    article_title = models.CharField(max_length=100)
    article_text = models.TextField()
    article_date_create = models.DateTimeField()
    article_date_modify = models.DateTimeField()
    article_access = models.BooleanField(default=True)
    article_autor = models.OneToOneField(User)


class Tags(models.Model):
    tags_name = models.CharField(max_length=50)
    tags_key = models.ForeignKey(Article)
