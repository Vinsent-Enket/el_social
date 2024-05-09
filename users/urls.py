from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, ProfileDetailView, SubscriptionsCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('reg/', RegisterView.as_view(), name='reg'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile_update/<int:pk>/', UserUpdateView.as_view(), name='profile_update'),
    path('subscribe/', SubscriptionsCreateView.as_view(), name='subscribe'),

]
