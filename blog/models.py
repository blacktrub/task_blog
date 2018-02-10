#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tags)
    count = models.ManyToManyField('CountArticle')

    def __str__(self):
        return self.title


class CountArticle(models.Model):
    user = models.OneToOneField(User)
    count_article = models.ManyToManyField(Article)


class Profile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
