from django.db import models
import random

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


