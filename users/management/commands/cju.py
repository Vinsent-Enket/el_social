
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Надо ли и тут прятать логины пароли в переменные окружения????"""
    def handle(self, *args, **options):

        first_name = ['John', 'Mike', 'Peter', 'Mary', 'Nate']
        last_name = ['Smith', 'Johnson', 'Jones', 'Williams', 'Brown']
        for i in range(5):
            user = User.objects.create(
                email=f'{first_name[i]}{last_name[i]}@gmail.com',
                first_name=first_name[i],
                last_name=last_name[i],
                telephone='+70000000' + str(i)
            )
            user.set_password('123qwe456rty')
            user.save()
