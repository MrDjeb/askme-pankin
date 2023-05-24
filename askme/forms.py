from django import forms
from django.forms.utils import ErrorList
from . import models
from django.contrib import messages



class LoginForm(forms.Form) :
    
    username = forms.CharField(label="Login")
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)