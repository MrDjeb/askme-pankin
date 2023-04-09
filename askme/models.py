from django.db import models

QUESTIONS = [
    {
        'title': f'Question{i}',
        'text': f'Text{i}'
    } for i in range(10)
]
