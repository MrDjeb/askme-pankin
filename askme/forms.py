from django import forms
from django.forms.utils import ErrorList
from . import models
from django.core.exceptions import ValidationError
from django.contrib import messages



class LoginForm(forms.Form) :
    
    username = forms.CharField(label="Login")
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name", "email", "avatar")

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile

        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        
        return profile.save()


class SingupForm(forms.ModelForm):
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = models.User
        fields = ("username", "email", "first_name", "last_name", "password", "password_check", "avatar")

    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            raise ValidationError('Passwords are not the same')

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile

        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']

        self.cleaned_data.pop('password_check')
        return profile.create()


