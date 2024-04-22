from django.test import TestCase
import unittest
from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse_lazy

from config import settings
from datetime import datetime, timedelta

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