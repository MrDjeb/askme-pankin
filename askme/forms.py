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

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            self.add_error('password_check', 'Password does not equal!')
            return False
        return True

    def save(self):
        avatar = self.cleaned_data['avatar']

        self.cleaned_data.pop('avatar')
        self.cleaned_data.pop('password_check')
        user = models.User.objects.create_user(**self.cleaned_data)
        user.set_password(self.cleaned_data['password'])

        profile = models.Profile.objects.create(user=user, avatar="avatars/avatar1.jpeg")
        if avatar:
            profile.avatar = avatar
        
        return profile.save()

class AskForm(forms.Form):
    title = forms.CharField(required=True, max_length=50, widget=forms.Textarea, help_text="How to generate website?")
    text = forms.CharField(required=True, max_length=500, widget=forms.Textarea, help_text="Have no idea about it...")
    tags = forms.CharField(required=True, max_length=50, widget=forms.Textarea, help_text="tag_1 tag_2 tag_3")

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        tags_array = tags.split()
        for tag in tags_array:
            if len(tag) > 16:
                self.add_error('tags', 'max length of one tag is 16 simbols')
                return

        return tags
    
    def save(self, request):
        profile = models.Profile.objects.get(user=models.User.objects.get(username=request.user))
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        tags_array = self.cleaned_data['tags'].split()
        tags = []
        
        question = models.Question.objects.create(profile=profile, title=title, text=text, rating=0)

        for t in tags_array:
            if models.Tag.objects.filter(title=t).exists():
                tag = models.Tag.objects.get(title=t)
                tag.count+=1
                tag.save()
            else:
                tag = models.Tag.objects.create(title=t, count=1)
            tags.append(tag)

        question.tags.set(tags)
        question.save()

        return question

class AnswerForm(forms.Form):
    answer = forms.CharField(required=True, max_length=500, help_text="Enter your answer here")

    def save(self, request, question_id):
        profile = models.Profile.objects.get(user=models.User.objects.get(username=request.user))
        question = models.Question.objects.get(id=question_id)
        return models.Answer.objects.create(profile=profile, text=self.cleaned_data['answer'], question=question, rating=0, is_right=False)
