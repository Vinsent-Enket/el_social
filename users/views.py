from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from rest_framework import generics, request
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Content
from transactions.models import Transaction
from users.forms import UserRegisterForm, UserProfileForm, SubscriptionForm
from users.models import User, Subscription
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permission import IsTrueUser
from users.serializers import UserSerializer, MyTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('social:main')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'author'
    success_url = reverse_lazy('users:profile')
    form_class = SubscriptionForm

    def get_initial(self):
        # Получаем объект пользователя по pk
        proprietor = self.request.user
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        # Предзаполняем данные формы
        initial_data = {
            'proprietor': proprietor,
            'author': author,
            # Добавьте другие поля, которые вы хотите предзаполнить
        }
        return initial_data

    def get_context_data(self, **kwargs):
        context = {}
        context['subscriptions'] = Subscription.objects.filter(proprietor=self.request.user)
        context['content_list'] = Content.objects.filter(author=kwargs['pk'])
        context['object'] = User.objects.get(pk=kwargs['pk'])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self.form_class(initial=self.get_initial())
        context['form'] = form
        form.fields['author'].queryset = User.objects.filter(pk=kwargs['pk'])
        form.fields['proprietor'].queryset = User.objects.filter(pk=self.request.user.pk)

        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Здесь вы можете сохранить данные в базу данных или выполнить другие действия
            print(form.cleaned_data)
            return redirect('users:profile', pk=pk)
        else:
            return render(request, self.template_name, {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    # TODO выключить возможность редактировать кошелек, уровень автора и тд
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

# class UserCreateAPIView(generics.CreateAPIView):
#     """
#     Создание пользователя
#     """
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer
#
#
# class UserRetrieveAPIView(generics.RetrieveAPIView):
#     permission_classes = [IsTrueUser, IsAuthenticated]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = [IsTrueUser, IsAuthenticated]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserDestroyAPIView(generics.DestroyAPIView):
#     permission_classes = [IsTrueUser, IsAuthenticated]
#     queryset = User.objects.all()
#
#
# class UserCheckLevelAPIView(APIView):
#     permission_classes = [IsTrueUser, IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):  # TODO надо ли переносить этот метод в сериализатор?
#         user = self.request.user
#         count = Subscription.objects.filter(author=user).count()
#         if count >= 10:
#             user.author_level = 1
#         elif count >= 50:
#             user.author_level = 2
#         elif count >= 100:
#             user.author_level = 3
#         user.save()
#         return Response({"message": f"Ваш уровень как автора {user.author_level}"})
#
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#
#
# class UpdateTelegramChatIdAPIView(APIView):
#     def post(self, *args, **kwargs):
#         user = self.request.user
#         chat_id = self.request.data.get('chat_id')
#         user.chat_id = chat_id
#         user.save()
#
#         return Response({'message': f'Чат {chat_id} в телеграмме успешно привязан'})
#
#
# class SubscriptionAPIView(APIView):
#     def post(self, *args, **kwargs):
#         user = self.request.user
#         author = User.objects.get(pk=self.request.data.get('author'))
#         level = self.request.data.get('level')
#         print(user, author, level)
#         if Subscription.objects.filter(proprietor=user.id, author=author.id, level=level).exists():
#             print('exists')
#             return Response({'message': 'Вы уже подписаны на этого автора'})
#         user.wallet -= 100 * level  # TODO сделать проверку кошелька
#         subscription = Subscription(author=author, level=level, proprietor=user).save()
#         return Response({'message': f'Вы получили подписку {level} уровня на {author.name}'})
