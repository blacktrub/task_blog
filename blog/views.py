#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article, CountArticle, Profile
from django.contrib.auth.models import User
from .forms import RegisterForm, NewPostForm, EditPostForm, RepeatEmailForm
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from .decorators import access_private_post
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from .tools import send_email_auth


class HomeView(generic.ListView):
    template_name = 'blog/home.html'
    context_object_name = 'post_blog'

    def get_queryset(self):
        return Article.objects.order_by('-created').all()


def article_detail(request, pk):
    obj = get_object_or_404(Article, pk=pk)

    @access_private_post(url='/access_error_to_post', access=obj.is_private)
    def view(request, obj):
        if request.user.is_authenticated():
            count_object = CountArticle.objects.get(user=request.user)
            count_object.count.remove(obj)
        return render(request, 'blog/full.html', {'fullpost_blog': obj})

    return view(request, obj)


def access_error_to_post(request):
    return render(request, 'blog/access_error_to_post.html')


def access_error_to_modify(request):
    return render(request, 'blog/access_error_to_modify.html')


def error_expired(request):
    return render(request, 'blog/error_expired.html')


def success_register_account(request):
    return render(request, 'blog/success_register_account.html')


def success_activated_account(request):
    return render(request, 'blog/success_activated_account.html')


class EditView(generic.ListView):
    template_name = 'blog/edit.html'
    context_object_name = 'edit_post'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.order_by('-created').all()
        else:
            return Article.objects.filter(author=self.request.user)\
                .order_by('-created')

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditView, self).dispatch(request, *args, **kwargs)


@login_required(redirect_field_name='',
                login_url='/access_error_to_post')
def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user.is_superuser:
        article.delete()
        return HttpResponseRedirect('/edit')
    elif request.user == article.author:
        article.delete()
        return HttpResponseRedirect('/edit')
    return HttpResponseRedirect('/access_error_to_modify')


class RegisterView(FormView):
    template_name = 'blog/reg.html'
    form_class = RegisterForm
    success_url = '/success_register_account'

    def form_valid(self, form):
        form.clean_email()
        form.clean_password2()
        form.save()

        user = User.objects.get(username=form.cleaned_data['username'])
        send_email_auth(user=user)

        return super(RegisterView, self).form_valid(form)


class RepeatEmailView(FormView):
    template_name = 'blog/repeat_email.html'
    form_class = RepeatEmailForm
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])
        if not user.is_active:
            send_email_auth(user=user, auth=True)

        return super(RepeatEmailView, self).form_valid(form)


def confirm_registration(request, activation_key):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user_profile = get_object_or_404(Profile,
                                     activation_key=activation_key)
    if user_profile.user.is_active:
        return HttpResponseRedirect('/')
    if user_profile.key_expires < timezone.now():
        return HttpResponseRedirect('/error_expired')
    user = user_profile.user
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/success_activated_account')


class NewPostView(FormView):
    template_name = 'blog/newpost.html'
    form_class = NewPostForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.title = form.cleaned_data["title"]
        f.text = form.cleaned_data["text"]
        f.is_private = form.cleaned_data["is_private"]
        f.author = self.request.user
        f.save()
        f.tags = list(form.cleaned_data["tags"])

        article = Article.objects.get(article_title=form.cleaned_data["title"])
        article.countarticle_set.add(*list(CountArticle.objects.all()))

        form.save_m2m()

        return HttpResponseRedirect('/edit')

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(NewPostView, self).dispatch(request, *args, **kwargs)


class EditPostView(UpdateView):
    form_class = EditPostForm
    template_name = 'blog/editpost.html'
    model = Article
    success_url = '/edit'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.modified = timezone.now()
        f.tags = list(form.cleaned_data["tags"])
        f.save()
        return redirect(self.get_success_url())

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditPostView, self).dispatch(request, *args, **kwargs)
