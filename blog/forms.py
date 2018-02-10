#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Article
from django.contrib.auth import password_validation
from django import forms
from django_summernote.widgets import SummernoteWidget


class RepeatEmailForm(ModelForm):

    class Meta:
        model = User
        fields = ("email",)


class EditPostForm(ModelForm):

    class Meta:
        model = Article
        fields = ("article_title", "article_text",
                  "article_access", "article_tag")


class NewPostForm(ModelForm):

    class Meta:
        model = Article
        fields = ("article_title", "article_text",
                  "article_access", "article_tag")
        widgets = {
            'article_text': SummernoteWidget(),
        }

    def save(self, commit=True):
        article = super(NewPostForm, self).save(commit=False)
        if commit:
            article.save()
        return article


class RegisterForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
        'email_error': "Пользователь с таким e-mail уже существует",
    }
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
        )
    password2 = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput,
        )

    class Meta:
        model = User
        fields = ("username", "email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_error'],
                code='email_error',
                )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'),
                                              self.instance)
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user
