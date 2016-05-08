#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import CountArticle, Article
from django.core.exceptions import ObjectDoesNotExist


def total_count(request):

    def init_count(request):
        #  add to CountArticle model Article list
        count = CountArticle.objects
        usr = request.user
        art = Article.objects.all()
        art_add = Article.objects
        count.create(user=usr)
        count = CountArticle.objects.get(user=usr)
        for x in art:
            count.count.add(art_add.get(article_title=x))
        return {"total_count": count.count.all().count(), }

    if request.user.is_authenticated():
        try:
            total = CountArticle.objects.get(user=request.user)
            return {"total_count": total.count.all().count(), }
        except ObjectDoesNotExist:
            return init_count(request)
    return {}
