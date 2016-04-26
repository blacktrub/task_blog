#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.models import User


class Article(models.Model):
    article_title = models.CharField(max_length=100)
    article_text = models.TextField()
    article_date_create = models.DateTimeField(default=timezone.now)
    article_date_modify = models.DateTimeField(default=timezone.now)
    article_access = models.BooleanField(default=True)
    article_autor = models.OneToOneField(User)


class Tags(models.Model):
    tags_name = models.CharField(max_length=50)
    tags_key = models.ForeignKey(Article)
