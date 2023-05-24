from django.db import models
from django.contrib.auth.models import User
import random

class ProfileManager(models.Manager):
    def get_top(self):
        members = self.annotate(models.Count('answer')).order_by('-answer__count')[:10]
        if members:
            for m in members.iterator():
                m.font_size = f'{random.randint(6, 25)}'
        return members

    def get_auth(self, request):
        if request.user.is_authenticated:
            return self.get(user=User.objects.get(username=request.user))
        else:
            return None

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, default="static/img/avatar1.jpeg", upload_to="static/img")

    objects = ProfileManager()
    
    font_size = ''

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_top(self):
        #tags = self.annotate(models.Count('question')).order_by('-question__count')[:10]
        tags = self.order_by('-count')[:10]
        if tags:
            for t in tags.iterator():
                # TODO размер тега от его популярности
                t.font_size = f'{random.randint(6, 25)}' #t | {'font_size': f'{random.randint(6, 25)}'}
        return tags



class Tag(models.Model):
    title = models.CharField(max_length=16)
    count = models.IntegerField()

    objects = TagManager()

    font_size = ''

    def __str__(self):
        return f"{self.title}"


class QuestionManager(models.Manager):
    def by_created_at(self):
        return self.order_by('-created_at')

    def by_rating(self):
        return self.order_by('-rating')

    def by_tag(self, tag_title):
        return self.filter(tags__title = tag_title)

class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()

    def __std__(self):
        return f'Question {self.title}'


class AnswerManage(models.Manager):
    def get_answers(self, question):
        return Answer.objects.filter(question=question)

class Answer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    is_right = models.BooleanField()

    objects = AnswerManage()


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.BooleanField()