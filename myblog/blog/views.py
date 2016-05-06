#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article, Tags
from django.contrib.auth.models import User
from .forms import RegisterForm, NewPostForm
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from .decorators import access_private_post
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


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


def Access_error_to_post(request):
    return render(request, 'blog/access_error_to_post.html')


class EditView(generic.ListView):
    template_name = 'blog/edit.html'
    context_object_name = 'edit_post'

    def get_queryset(self):
        return Article.objects.all()

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditView, self).dispatch(request, *args, **kwargs)


@login_required(redirect_field_name='',
                login_url='/access_error_to_post')
def DeletePost(request, pk):
    Article.objects.get(pk=pk).order_by('-article_date_create').delete()
    return HttpResponseRedirect('/edit')


class RegisterView(FormView):
    template_name = 'blog/reg.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        form.clean_email()
        form.clean_password2()
        form.save(commit=False)
        return super(RegisterView, self).form_valid(form)


class NewPostView(FormView):
    template_name = 'blog/newpost.html'
    form_class = NewPostForm
    success_url = '/'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.article_title = form.cleaned_data["article_title"]
        f.article_text = form.cleaned_data["article_text"]
        f.article_access = form.cleaned_data["article_access"]
        f.article_autor = self.request.user
        f.save()

        tags = form.cleaned_data['article_tag']
        for tag in range(len(tags)):
            tag_add = Tags.objects.get(tags_name=tags[tag])
            f.article_tag.add(tag_add)

        form.save_m2m()

        return HttpResponseRedirect('/edit')

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(NewPostForm, self).dispatch(request, *args, **kwargs)
