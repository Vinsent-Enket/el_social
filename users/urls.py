from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    MyTokenObtainPairView, UpdateTelegramChatIdAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', UserCreateAPIView.as_view(), name='user_create'),
    path('profile/<int:pk>/', UserRetrieveAPIView.as_view(), name='profile'),
    path('profile_update/<int:pk>/', UserUpdateAPIView.as_view(), name='profile_update'),
    path('profile/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='profile_delete'),

    # новые урлы для пользователя
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('chat_id/', UpdateTelegramChatIdAPIView.as_view(), name='chat_id'),



]
