from django.urls import reverse_lazy
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase, force_authenticate, APIClient

from social.models import Comment, Content
from users.models import User


class LikeTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "telephone": "+79244562345",
            "name": "Aboba",
            "email": "aboba@test.ru",
            "description": "Просто амогус",
            "password": "Qwert12345"
        }
        response = self.client.post(reverse_lazy('users:user_create'), self.user_data, format='json')
        self.user = User.objects.get(id=response.data.get('id'))
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.content_data = {
            "name": "Тест пост",
            "text": "Тест текст",
            "author": self.user,

        }
        self.content = Content.objects.create(**self.content_data)
        self.like_data = {
            "content": self.content,
            "author": self.user,
        }
        self.like = Comment.objects.create(**self.like_data)

    def test_like(self):
        data = {"content_id": self.content.id}
        response = self.client.post(reverse_lazy('social:like'), data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.post(reverse_lazy('social:like'), data)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
