from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from rest_framework import generics, request
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from users.forms import UserRegisterForm, UserProfileForm, SubscriptionForm
from users.models import User, Subscription
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permission import IsTrueUser
from users.serializers import UserSerializer, MyTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.

class UserProfileView(UpdateView):
    model = User
    form_class = UserChangeForm

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            if form.data.get('need_generate', False):
                self.object.set_password(
                    self.object.make_random_password(length=12)
                )
                self.object.save()

        return super().form_valid(form)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('social:main')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = Subscription.objects.filter(proprietor=self.request.user)
        return context


class ProfileView(UpdateView):  # TODO выключить возможность редактировать кошелек, уровень автора и тд
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class SubscriptionsCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'users/subscription_form.html'
    success_url = reverse_lazy('social:main')





"""
--------------------------------------------------------------------------------------------------
"""


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


class UserCheckLevelAPIView(APIView):
    permission_classes = [IsTrueUser, IsAuthenticated]

    def get(self, request, *args, **kwargs):  # TODO надо ли переносить этот метод в сериализатор?
        user = self.request.user
        count = Subscription.objects.filter(author=user).count()
        if count >= 10:
            user.author_level = 1
        elif count >= 50:
            user.author_level = 2
        elif count >= 100:
            user.author_level = 3
        user.save()
        return Response({"message": f"Ваш уровень как автора {user.author_level}"})


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
        author = User.objects.get(pk=self.request.data.get('author'))
        level = self.request.data.get('level')
        print(user, author, level)
        if Subscription.objects.filter(proprietor=user.id, author=author.id, level=level).exists():
            print('exists')
            return Response({'message': 'Вы уже подписаны на этого автора'})
        user.wallet -= 100 * level  # TODO сделать проверку кошелька
        subscription = Subscription(author=author, level=level, proprietor=user).save()
        return Response({'message': f'Вы получили подписку {level} уровня на {author.name}'})
