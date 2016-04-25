#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_autor = models.CharField(max_length=50)
    article_tag = models.CharField(max_length=50)
    article_access = models.BooleanField()


class Tags(models.Model):
    tags_name = models.CharField(max_length=50)


class User(models.Model):
    user_name = models.CharField(max_length=50)
    user_group = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)


class Group(models.Model):
    group_name = models.CharField(max_length=50)
    group_access = models.BooleanField()
