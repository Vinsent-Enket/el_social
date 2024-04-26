from rest_framework import status
from rest_framework.reverse import reverse_lazy

import unittest
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command

from users.models import User
from rest_framework.test import APITestCase, force_authenticate, APIClient

from users.permission import IsTrueUser
from users.views import UserRetrieveAPIView


# Create your tests here.


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "telephone": "+79244562345",
            "name": "Aboba",
            "email": "aboba@test.ru",
            "description": "Просто амогус",
            "password": "Qwert12345"
        }
        response = self.client.post(reverse_lazy('users:user_create'), self.data, format='json')
        self.user = User.objects.get(id=response.data.get('id'))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_token(self):
        data_for_token = {"telephone": "+79244562345",
                          "password": "Qwert12345"}
        response = self.client.post(reverse_lazy('users:token_obtain_pair'), data_for_token, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile(self):
        response = self.client.get(reverse_lazy('users:profile', args=(self.user.id,)))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update(self):
        data = {
            "telephone": "+79244562345",
            "name": "Neaboba",
            "email": "aboba@test.ru",
            "description": "Просто амогус",
            "password": "Qwert12345"
        }
        response = self.client.put(reverse_lazy('users:profile_update', args=(self.user.id,)), data, format='json')
        # print(response.data)
        self.assertEqual(response.data.get('name'), 'Neaboba')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_delete(self):
        response = self.client.delete(reverse_lazy('users:profile_delete', args=(self.user.id,)))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)





class CommandTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('migrate', verbosity=0, interactive=False)

    def test_create_moderator_group(self):
        # Проверяем, что группа 'Moderator' не существует
        self.assertFalse(Group.objects.filter(name='Moderator').exists())

        # Вызываем команду
        call_command('cmg')

        # Проверяем, что группа 'Moderator' была создана
        self.assertTrue(Group.objects.filter(name='Moderator').exists())

        # Проверяем, что группе 'Moderator' были назначены соответствующие права
        add_permissions = Permission.objects.filter(codename__startswith='add_')
        change_permissions = Permission.objects.filter(codename__startswith='change_')
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        permissions_count = add_permissions.count() + change_permissions.count() + view_permissions.count()
        manager_group = Group.objects.get(name='Moderator')
        self.assertEqual(manager_group.permissions.count(), permissions_count)
