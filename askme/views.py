from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    context = {
        'islogin': True,
        'tags': models.TAGS,
        'members': models.MEMBERS,
        'questions': models.QUESTIONS,
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    context = {
        'question': models.QUESTIONS[question_id]
    }
    return render(request, 'question.html', context)
