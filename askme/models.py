from django.db import models
from django.contrib.auth.models import User
import random

class QuestionManager(models.Manager):
    def get_index(self):
        return self

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField
    rating = models.IntegerField
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey('Tag', null=True, on_delete=models.SET_NULL)

    objects = QuestionManager()

    def __std__(self):
        return f'Question {self.title}'


class Answer(models.Model):
    text = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField
    is_right = models.BooleanField

class Tag(models.Model):
    title = models.CharField(max_length=255)
    count = models.IntegerField
    
class User(models.Model):
    profile = models.OneToOneField(User, on_delete=models.PROTECT)
    mickname = models.CharField(max_length=255)
    avatar = models.ImageField

TAGS = [
    {
        'title': f'Tag{i}',
        'font_size': f'{random.randint(6, 25)}'
    } for i in range(10)
]

MEMBERS = [
    {
        'title': f'Member{i}',
    } for i in range(10)
]

QUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question{i}',
        'text': f'Text{i}'
    } for i in range(10)
]

BASE_CONTEXT = {
        'islogin': False,
        'tags': TAGS,
        'members': MEMBERS,
}


