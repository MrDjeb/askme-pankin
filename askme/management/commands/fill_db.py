from faker import Faker
from random import choice,randint
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from askme import models



class Command(BaseCommand):
    help = 'Fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"][0]
        self.stdout.write("Start fill database... with " + str(ratio) + " ratio.")
        fk = Faker() 

        users = [
            User(
                username=fk.user_name(),
                #password=fk.password(),
                email=fk.email(),
                first_name=fk.first_name(),
                last_name=fk.last_name(),
            ) for i in range(ratio)
        ]

        for u in users:
            u.set_password(fk.password())

        ava = "avatars/avatar1.jpeg"
        profiles = [
            models.Profile(
                user=users[i],
                avatar=ava,
            ) for i in range(ratio)
        ]
        
        #for p in profiles:
        #    self.stdout.write(p.user.username)
        User.objects.bulk_create(users)
        models.Profile.objects.bulk_create(profiles)
        self.stdout.write("Generated profiles")

        tags = [
            models.Tag(
                title=fk.license_plate(),
                count=randint(0, ratio),
            ) for _ in range(ratio)
        ]
        models.Tag.objects.bulk_create(tags)
        self.stdout.write("Generated tags")

        questions = [
            models.Question(
                profile=choice(profiles),
                title = fk.catch_phrase(),
                text = fk.text(max_nb_chars=1000),
                rating = randint(0, ratio),
                created_at = fk.date_time(),
            ) for i in range(ratio*10)
        ]

        models.Question.objects.bulk_create(questions)
        
        for q in questions:
            for _ in range(0, randint(0, 3)):
                q.tags.add(choice(tags))

        self.stdout.write("Generated questions")

        answers = [
            models.Answer(
                question=choice(questions),
                profile=choice(profiles),
                text=fk.text(),
                rating=randint(0, ratio),
                created_at=fk.date_time(),
                is_right=choice([True, False]),
            ) for i in range(ratio*100)
        ]
        models.Answer.objects.bulk_create(answers)
        self.stdout.write("Generated answers")

        likeQuestions = []
        for quest in questions:
            for i in range(quest.rating):
                likeQuestions.append(models.LikeQuestions(
                    profile=profiles[i],
                    question=quest,
                    type=True,
                ))
        models.LikeQuestions.objects.bulk_create(likeQuestions)
        self.stdout.write("Generated LikeQuestions")

        likeAnswers = []
        for ans in answers:
            for i in range(ans.rating):
                likeAnswers.append(models.LikeAnswers(
                    profile=profiles[i],
                    answer=ans,
                    type=True,
                ))
        models.LikeAnswers.objects.bulk_create(likeAnswers)
        self.stdout.write("Generated LikeAnswers")
                



#   пользователей — равное ratio;
#   вопросов — ratio * 10;
#   ответы — ratio * 100;
#   тэгов - ratio;
#   оценок пользователей - ratio * 200;

