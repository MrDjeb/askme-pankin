from django.db import models
from django.contrib.auth.models import User
import random

class ProfileManager(models.Manager):
    def best(self):
        return self.annotate(models.Count('answer')).order_by('-answer__count')[:10]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="static/img")

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

class TagManager(models.Manager):
    def popular(self):
        return self.annotate(models.Count('question')).order_by('-question__count')[:10]

class Tag(models.Model):
    title = models.CharField(max_length=16)
    count = models.IntegerField()

    objects = TagManager()

    def __str__(self):
        return f"{self.title}"

class QuestionManager(models.Manager):
    def by_created_at(self):
        return self.order_by('-created_at')

    def by_rating(self):
        return self.order_by('-rating')

    def by_tag(self, title):
        return self.filter(tag__title = title)

    def get_index(self):
        return self

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


class Answer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    is_right = models.BooleanField()

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.BooleanField()


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

ANSWERS = [
    {
        'id': f'{i}',
        'title': f'Question{i}',
        'text': f'Text{i}'
    } for i in range(67)
]

QUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question{i}',
        'text': f'Text{i}'
    } for i in range(55)
]


BASE_CONTEXT = {
        'islogin': False,
        'tags': TAGS,
        'members': MEMBERS,
}


