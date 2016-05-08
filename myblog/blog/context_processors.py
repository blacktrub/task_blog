#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import CountArticle, Article


def total_count(request):

    def init_count(request):
        #  add to CountArticle model
        count = CountArticle.objects
        usr = request.user
        art = Article.objects.all()
        total_art = []
        for a in range(len(art)):
            art_add = Article.objects.get(article_title=art[a])
            total_art.append(art_add)
        count.create(user=usr)
        count.get(user=usr)
        count.count = total_art
        return 1

    if request.user.is_authenticated():
        try:
            total = CountArticle.objects.get(user=request.user)
            return {"total_count": len(total.count.all()), }
        except:
            if init_count(request):
                total_count(request)

    return {}
