#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tags(models.Model):
    tags_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tags_name


class Article(models.Model):
    article_title = models.CharField(max_length=100)
    article_text = models.TextField()
    article_date_create = models.DateTimeField(default=timezone.now)
    article_date_modify = models.DateTimeField(default=timezone.now)
    article_access = models.BooleanField(default=True)
    article_autor = models.ForeignKey(User)
    article_tag = models.ManyToManyField(Tags)

    def __str__(self):
        return self.article_title
