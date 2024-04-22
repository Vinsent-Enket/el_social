from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Надо ли и тут прятать логины пароли в переменные окружения????"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='Admin@django.ru',
            is_staff=True,
            is_superuser=True,
            telephone='+79999999999',
        )
        user.set_password('123qwe456rty')
        user.save()
