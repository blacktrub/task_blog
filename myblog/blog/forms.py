#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms


class RegisterForm(ModelForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
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
        help_text="Введите одинаковые пароли"
        )
    email = forms.EmailField(
        label="Адрес электронной почты",
        strip=False,
        widget=forms.EmailInput,
        )

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
