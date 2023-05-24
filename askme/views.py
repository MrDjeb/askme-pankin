from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from . import models
from . import forms

from django.forms.models import model_to_dict
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

def paginate(objects_list, request, per_page=10):

    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

BASE_CONTEXT = {
        'tags': models.Tag.objects.get_top(),
        'members': models.Profile.objects.get_top(),
}

def index(request):
    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request=request),
        'page_obj': paginate(models.Question.objects.by_created_at(), request)
    }

    return render(request, 'index.html', context)

def tag(request, tag_title):
    questions = models.Question.objects.by_tag(tag_title)
    if not questions:
        raise Http404(f'Tag: {tag_title} does not exist')

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'page_obj': paginate(questions, request)
    }
    return render(request, 'index.html', context)

def hot(request):
    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'page_obj': paginate(models.Question.objects.by_rating(), request)
    }
    return render(request, 'index.html', context)



def log_in(request):
    print(request.POST)
    if request.method == 'GET':
        login_form = forms.LoginForm()
    elif request.method == 'POST': 
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'form': login_form,
    }
    return render(request, 'login.html', context)

@login_required(login_url='/login/')
def log_out(request):
    auth.logout(request)
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect(reverse('index'))

@require_http_methods(['GET', 'POST'])
def signup(request):

    profile_data = models.Profile.objects.get_auth(request)
    if profile_data:
        redirect(reverse('index'))

    if request.method == 'GET':
        signup_form = forms.SingupForm()
    elif request.method == 'POST':
        signup_form = forms.SingupForm(request.POST, files=request.FILES, instance=request.user)
        if signup_form.is_valid():
            signup_form.save()
            print(signup_form)
            return redirect('settings')

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'form': signup_form,
    }
    return render(request, 'signup.html', context)


@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def settings(request):

    profile_data = models.Profile.objects.get_auth(request)
    if request.method == 'GET':
        data = model_to_dict(profile_data.user)
        #data['avatar'] = profile_data.avatar.url
        #print(data)
        settings_form = forms.SettingsForm(initial=data)

    elif request.method == 'POST':
        settings_form = forms.SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')
        
    context = BASE_CONTEXT | {
        'profile_data': profile_data,
        'form': settings_form,
    }
    return render(request, 'settings.html', context)



def question(request, question_id):
    try:
        q = models.Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        raise Http404(f'Question_id {question_id} does not exist')

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'question': q,
        'page_obj': paginate(models.Answer.objects.get_answers(q), request, 5)
    }
    return render(request, 'question.html', context)

@login_required(login_url='/login/')
def ask(request):
    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
    }
    return render(request, 'ask.html', context)



    
