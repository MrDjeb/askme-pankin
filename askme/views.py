from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import Http404

from django.db.models import ObjectDoesNotExist
from . import models

def paginate(objects_list, request, per_page=10):

    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

BASE_CONTEXT = {
        'islogin': False,
        'tags': models.Tag.objects.get_top(),
        'members': models.Profile.objects.get_top(),
}

def index(request):
    context = BASE_CONTEXT | {
        'page_obj': paginate(models.Question.objects.by_created_at(), request)
    }

    return render(request, 'index.html', context)

def tag(request, tag_title):
    questions = models.Question.objects.by_tag(tag_title)
    if not questions:
        raise Http404(f'Tag: {tag_title} does not exist')

    context = BASE_CONTEXT | {
        'page_obj': paginate(questions, request)
    }
    return render(request, 'index.html', context)

def hot(request):
    context = BASE_CONTEXT | {
        'page_obj': paginate(models.Question.objects.by_rating(), request)
    }
    return render(request, 'index.html', context)

def login(request):
    context = BASE_CONTEXT | {
    }
    return render(request, 'login.html', context)

def signup(request):
    context = BASE_CONTEXT | {
    }
    return render(request, 'signup.html', context)

def settings(request):
    context = BASE_CONTEXT | {
    }
    return render(request, 'settings.html', context)

def question(request, question_id):
    try:
        q = models.Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        raise Http404(f'Question_id {question_id} does not exist')

    context = BASE_CONTEXT | {
        'question': q,
        'page_obj': paginate(models.Answer.objects.get_answers(q), request, 5)
    }
    return render(request, 'question.html', context)

def ask(request):
    context = BASE_CONTEXT | {
    }
    return render(request, 'ask.html', context)



    
