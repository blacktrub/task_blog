#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import CountArticle, Article
from django.core.exceptions import ObjectDoesNotExist


def total_count(request):
    if request.user.is_authenticated():
        try:
            total = CountArticle.objects.get(user=request.user)
            return {"total_count": total.count_article.all().count(), }
        except ObjectDoesNotExist:
            CountArticle.objects.create(user=request.user)
            count_object = CountArticle.objects.get(user=request.user)
            art = Article.objects.all()
            art = list(art)
            count_object.count_article.add(*list(Article.objects.all()))
            return {"total_count": count_object.count_article.all().count(), }
    return {}
