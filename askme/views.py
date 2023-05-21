from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from . import models

def paginate(objects_list, request, per_page=10):

    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

def index(request):
    context = models.BASE_CONTEXT | {

        'page_obj': paginate(models.QUESTIONS, request)
    }

    return render(request, 'index.html', context)

def login(request):
    context = models.BASE_CONTEXT | {
    }
    return render(request, 'login.html', context)

def signup(request):
    context = models.BASE_CONTEXT | {
    }
    return render(request, 'signup.html', context)

def settings(request):
    context = models.BASE_CONTEXT | {
    }
    return render(request, 'settings.html', context)

def question(request, question_id):
    context = models.BASE_CONTEXT | {
        'question': models.QUESTIONS[question_id],
        'page_obj': paginate(models.ANSWERS, request, 5)
    }
    return render(request, 'question.html', context)

def tag(request, tag_title):
    context = models.BASE_CONTEXT | {
        'questions': models.QUESTIONS,
    }
    return render(request, 'index.html', context)

def hot(request):
    context = models.BASE_CONTEXT | {
        'questions': models.QUESTIONS,
    }
    return render(request, 'index.html', context)

def ask(request):
    context = models.BASE_CONTEXT | {
    }
    return render(request, 'ask.html', context)



    
