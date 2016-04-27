#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tags(models.Model):
    tags_name = models.CharField(max_length=50)


class Article(models.Model):
    article_title = models.CharField(max_length=100)
    article_text = models.TextField()
    article_date_create = models.DateTimeField(default=timezone.now)
    article_date_modify = models.DateTimeField(default=timezone.now)
    article_access = models.BooleanField(default=True)
    article_autor = models.OneToOneField(User)
    article_tag = models.ManyToManyField(Tags)
