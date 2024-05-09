from django.urls import reverse_lazy
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase, force_authenticate, APIClient

from social.models import Comment, Content
from users.models import User


class CommentTestCase(APITestCase):
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
        self.comment_data = {
            "content": self.content,
            "text": "Тест текст",
            "author": self.user,
        }
        self.comment = Comment.objects.create(**self.comment_data)

    def test_comment_create(self):
        self.comment_data['content'] = self.content.id
        response = self.client.post('http://127.0.0.1:8000/social/comment/', self.comment_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_comment_list(self):
        response = self.client.get('http://127.0.0.1:8000/social/comment/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_comment_detail(self):
        response = self.client.get(f'http://127.0.0.1:8000/social/comment/{self.comment.id}/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_comment_update(self):
        self.comment_data['text'] = "Другой текст"
        self.comment_data['content'] = self.content.id
        response = self.client.put(f'http://127.0.0.1:8000/social/comment/{self.comment.id}/', self.comment_data)
        self.assertEqual(response.data.get('text'), "Другой текст")

    def test_comment_partial_update(self):
        self.comment_data['text'] = "Другой текст2"
        self.comment_data['content'] = self.content.id
        response = self.client.patch(f'http://127.0.0.1:8000/social/comment/{self.comment.id}/', self.comment_data)
        self.assertEqual(response.data.get('text'), "Другой текст2")

    def test_comment_delete(self):
        response = self.client.delete(f'http://127.0.0.1:8000/social/comment/{self.comment.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
