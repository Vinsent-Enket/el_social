from django.core.management import BaseCommand
from itertools import chain
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Получаем группу по имени
        try:
            manager_group = Group.objects.get(name='Moderator')
            # Удаляем группу
            manager_group.delete()
        except Group.DoesNotExist:
            print("Группа 'Moderator' не существует.")

        manager_group = Group.objects.create(name='Moderator')
        # Получение прав на просмотр всех категорий и моделей без возможности изменения
        add_permissions = Permission.objects.filter(codename__startswith='add_')
        change_permissions = Permission.objects.filter(codename__startswith='change_')
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        all_permissions = chain(add_permissions, change_permissions, view_permissions)
        manager_group.permissions.set(all_permissions)

        manager_group.save()
        print("Группа 'Moderator' создана.")
