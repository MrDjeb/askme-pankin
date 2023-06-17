from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import ObjectDoesNotExist
from . import models
from . import forms
import json

from django.forms.models import model_to_dict
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

def paginate(objects_list, request, per_page=10):

    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
try:
    BASE_CONTEXT = {
        
            'tags': models.Tag.objects.get_top(),
            'members': models.Profile.objects.get_top(),
    }
except:
    BASE_CONTEXT = {
        'tags':models.TagManager,
        'members': models.ProfileManager,
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
        redirect('index')

    if request.method == 'GET':
        signup_form = forms.SingupForm()
    elif request.method == 'POST':
        signup_form = forms.SingupForm(request.POST, files=request.FILES)
        if signup_form.is_valid() and signup_form.clean_repeat_password():
            signup_form.save()
            user = auth.authenticate(request=request, **signup_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect('/settings/')

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

    if request.method == 'GET':
        answer_form = forms.AnswerForm()
    elif request.method == 'POST':
        if not models.Profile.objects.get_auth(request):
            return redirect(reverse('login'))
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.save(request, question_id)
            return redirect(reverse('question', args=[question_id]))

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'question': q,
        'page_obj': paginate(models.Answer.objects.get_answers(q), request, 5),
        'form': answer_form,
    }
    return render(request, 'question.html', context)


@login_required(login_url='/login/')
def ask(request):

    if request.method == 'GET':
        ask_form = forms.AskForm()
    elif request.method == 'POST':
        ask_form = forms.AskForm(request.POST)
        if ask_form.is_valid():
            question = ask_form.save(request)
            return redirect(reverse('question', args=[question.id]))

    context = BASE_CONTEXT | {
        'profile_data': models.Profile.objects.get_auth(request),
        'form': ask_form,
    }
    return render(request, 'ask.html', context)


@login_required()
@require_POST
def rating_set_question(request):
    data = json.loads(request.body.decode())

    try:
        question = models.Question.objects.get(id=data['question_id'])
    except models.Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)

    new_rating = question.rating

    isLike = models.LikeQuestions.objects.filter(question=question, profile=request.user.profile, type=data['type']).exists()

    if not isLike:
        isAntiLike = models.LikeQuestions.objects.filter(question=question, profile=request.user.profile, type=(not data['type'])).exists()
        if not isAntiLike:
            models.LikeQuestions.objects.create(question=question, profile=request.user.profile, type=data['type']).save()
        else:
            models.LikeQuestions.objects.get(question=question, profile=request.user.profile, type=(not data['type'])).delete()

        if data['type']:
            new_rating+=1
        else:
            new_rating-=1

    question.rating = new_rating

    question.save()
    return JsonResponse({
        'new_rating': new_rating
    })

@login_required()
@require_POST
def rating_set_answer(request):
    data = json.loads(request.body.decode())

    try:
        answer = models.Answer.objects.get(id=data['answer_id'])
    except models.Answer.DoesNotExist:
        return JsonResponse({'error': 'Answer_id not found'}, status=404)

    new_rating = answer.rating

    isLike = models.LikeAnswers.objects.filter(answer=answer, profile=request.user.profile, type=data['type']).exists()

    if not isLike:
        isAntiLike = models.LikeAnswers.objects.filter(answer=answer, profile=request.user.profile, type=(not data['type'])).exists()
        if not isAntiLike:
            models.LikeAnswers.objects.create(answer=answer, profile=request.user.profile, type=data['type']).save()
        else:
            models.LikeAnswers.objects.get(answer=answer, profile=request.user.profile, type=(not data['type'])).delete()

        if data['type']:
            new_rating+=1
        else:
            new_rating-=1

    answer.rating = new_rating

    answer.save()
    return JsonResponse({
        'new_rating': new_rating
    })

@login_required()
@require_POST
def correct_set_answer(request):
    data = json.loads(request.body.decode())

    try:
        answer = models.Answer.objects.get(id=data['answer_id'])
    except models.Answer.DoesNotExist:
        return JsonResponse({'error': 'Answer_id not found'}, status=404)

    if (request.user.profile == answer.question.profile):
        answer.is_right = not answer.is_right
        answer.save()
    else:
        return JsonResponse({'error': 'User is not author of this question'}, status=403)
    
    return JsonResponse({
        'answer_is_right': answer.is_right
    })


    
