#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article


class HomeView(generic.ListView):
    template_name = 'blog/home.html'
    context_object_name = 'post_blog'

    def get_queryset(self):
        return Article.objects.order_by('-article_date_create').all()


class FullView(generic.DetailView):
    template_name = 'blog/full.html'
    model = Article
    context_object_name = 'fullpost_blog'
