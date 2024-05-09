from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient

from social.models import Content
from users.models import User


# Create your api_tests here.
class ContentTestCase(APITestCase):
    def setUp(self) -> None:
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
        self.data = {
            "name": "Тест пост",
            "text": "Тест текст",

        }
        self.content = Content.objects.create(**self.data, author=self.user)

    def test_create_content(self):
        # вместо полного пути указать через reverse
        #self.data['author'] = self.user.id
        # response = self.client.post(reverse('social:content-create'), self.data, format='json')
        response = self.client.post('http://127.0.0.1:8000/social/content/', self.data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_content(self):
        # response = self.client.get('http://127.0.0.1:8000/social/content/')
        response = self.client.get(reverse('social:content-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_content(self):
        response = self.client.get(reverse('social:content-detail', kwargs={'pk': self.content.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_content(self):
        update_data = self.data
        update_data['text'] = "Тест текст2"
        update_data['author'] = self.user.id
        # response = self.client.put(reverse('social:content', kwargs={'pk': self.content.id}), update_data,
        #                            format='json')
        response = self.client.put(f'http://127.0.0.1:8000/social/content/{self.content.id}/', update_data,
                                   format='json', )
        # print(response.data)
        self.assertEqual(response.data['text'], update_data['text'])

    def test_partial_update_content(self):
        update_data = self.data
        update_data['text'] = "Тест текст3"
        update_data['author'] = self.user.id

        # response = self.client.patch(reverse('social:content-partial_update', kwargs={'pk': self.content.id}),
        # update_data, format='json')
        response = self.client.patch(f'http://127.0.0.1:8000/social/content/{self.content.id}/', update_data,
                                     format='json', )
        # print(response.data)
        self.assertEqual(response.data['text'], update_data['text'])


def test_delete_content(self):
    response = self.client.delete(reverse('social:content-destroy', kwargs={'pk': self.content.id}))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
