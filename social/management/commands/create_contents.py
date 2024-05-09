import random
import requests
from django.core.management import BaseCommand
from celery import shared_task
import django
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime, date

from config import settings
from social.models import Content, Comment, Like
from users.models import User
import time
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            for i in range(1, 4):
                content = Content.objects.create(
                    name=f'Тестовый контент {i} от {user.first_name}',
                    author=user,
                    text=f'Тестовый контент от {user.first_name} {user.last_name} {i}')
                content.save()
        for user in User.objects.all():
            for content in Content.objects.filter(~Q(author=user)):
                comment = Comment.objects.create(
                    content=content,
                    author=user,
                    text=f'Тестовый комментарий от {user.first_name} {user.last_name}'
                )
                comment.save()
                if random.randint(1, 3) == 3:
                    like = Like.objects.create(content=content, author=user)
                    like.save()
