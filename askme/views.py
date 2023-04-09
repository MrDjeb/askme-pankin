from django.shortcuts import render
from django.http import HttpResponse
from . import models

def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)
