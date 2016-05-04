#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article
from .forms import RegisterForm
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from .decorators import access_private_post


class HomeView(generic.ListView):
    template_name = 'blog/home.html'
    context_object_name = 'post_blog'

    def get_queryset(self):
        return Article.objects.order_by('-article_date_create').all()


def FullView(request, pk):
    obj = get_object_or_404(Article, pk=pk)

    @access_private_post(url='/access_error_to_post',
                         access=obj.article_access)
    def view(request, obj):
        return render(request, 'blog/full.html', {'fullpost_blog': obj})

    return view(request, obj)


class RegisterView(FormView):
    template_name = 'blog/reg.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        form.clean_email()
        form.clean_password2()
        form.save()
        return super(RegisterView, self).form_valid(form)


def Access_error_to_post(request):
    return render(request, 'blog/access_error_to_post.html')
