#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views import generic
from .models import Article, Tags, CountArticle, UserProfile
from django.contrib.auth.models import User
from .forms import RegisterForm, NewPostForm, EditPostForm
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from .decorators import access_private_post
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone


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
        if request.user.is_authenticated():
            count_object = CountArticle.objects.get(user=request.user)
            count_object.count_article.remove(obj)
        return render(request, 'blog/full.html', {'fullpost_blog': obj})

    return view(request, obj)


def Access_error_to_post(request):
    return render(request, 'blog/access_error_to_post.html')


def Access_error_to_modify(request):
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
            return Article.objects.order_by('-article_date_create').all()
        else:
            return Article.objects.filter(article_autor=self.request.user).order_by('-article_date_create')

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditView, self).dispatch(request, *args, **kwargs)


@login_required(redirect_field_name='',
                login_url='/access_error_to_post')
def DeletePost(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user.is_superuser:
        article.delete()
        return HttpResponseRedirect('/edit')
    elif request.user == article.article_autor:
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

        # Generate parameters for send email
        import hashlib, datetime, random
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        activation_key = hashlib.sha1(str(random.random()).encode()+email.encode()).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        user = User.objects.get(username=username)

        # Create UserProfile with parameters ^
        user_profile = UserProfile(user=user, activation_key=activation_key,
                                   key_expires=key_expires)
        user_profile.save()

        # Send email
        from django.core.mail import send_mail
        email_subject = 'Подтверждение регистрации'
        email_body = '''Привет %s, спасибо за регистрацию! Осталось всего чуть-чуть,
            перейди по ссылке:
            http://127.0.0.1:8000/confim/%s''' % (username, activation_key)
        send_mail(email_subject, email_body, 'blogdarkpy@gmail.com',
                  [email], fail_silently=False)

        return super(RegisterView, self).form_valid(form)


def reg_confim(request, activation_key):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
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
        f.article_title = form.cleaned_data["article_title"]
        f.article_text = form.cleaned_data["article_text"]
        f.article_access = form.cleaned_data["article_access"]
        f.article_autor = self.request.user
        f.save()

        tags = form.cleaned_data['article_tag']
        for tag in range(len(tags)):
            tag_add = Tags.objects.get(tags_name=tags[tag])
            f.article_tag.add(tag_add)

        article = Article.objects.get(article_title=form.cleaned_data["article_title"])
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
        f.article_date_modify = timezone.now()
        f.save()
        return redirect(self.get_success_url())

    @method_decorator(login_required(redirect_field_name='',
                      login_url='/access_error_to_post'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditPostView, self).dispatch(request, *args, **kwargs)
