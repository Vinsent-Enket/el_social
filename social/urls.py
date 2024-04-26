from django.urls import path, reverse

from rest_framework.routers import DefaultRouter

from social.apps import SocialConfig
from social.views import ContentViewSet, index, CommentViewSet, LakeAPIView

app_name = SocialConfig.name


router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'comment', CommentViewSet, basename='comment')
urlpatterns = [path('main/', index, name='index'),
               path('like/', LakeAPIView.as_view(), name='like'),
               ] + router.urls

