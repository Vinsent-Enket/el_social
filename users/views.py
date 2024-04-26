from django.shortcuts import render
from rest_framework import generics, request
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permission import IsTrueUser
from users.serializers import UserSerializer, MyTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.

class UserCreateAPIView(generics.CreateAPIView):
    """
    Создание пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsTrueUser, IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsTrueUser, IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsTrueUser, IsAuthenticated]
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UpdateTelegramChatIdAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        chat_id = self.request.data.get('chat_id')
        user.chat_id = chat_id
        user.save()

        return Response({'message': f'Чат {chat_id} в телеграмме успешно привязан'})



class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        author = self.request.data.get('author')



