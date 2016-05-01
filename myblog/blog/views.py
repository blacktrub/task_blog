#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article
from .forms import RegisterForm
from django.views.generic.edit import FormView


class HomeView(generic.ListView):
    template_name = 'blog/home.html'
    context_object_name = 'post_blog'

    def get_queryset(self):
        return Article.objects.order_by('-article_date_create')[:10]


class FullView(generic.DetailView):
    template_name = 'blog/full.html'
    model = Article
    context_object_name = 'fullpost_blog'


class RegisterView(FormView):
    template_name = 'blog/reg.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        form.clean_password2()
        form.save()
        return super(RegisterView, self).form_valid(form)
