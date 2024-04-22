import requests
from django.core.management import BaseCommand
from celery import shared_task
import django
from django.utils import timezone
from datetime import timedelta, datetime, date

from config import settings
from users.models import User
import time
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('hi')
