from django.urls import path, reverse

from rest_framework.routers import DefaultRouter

from social.apps import SocialConfig
from social.views import ContentViewSet, index, CommentViewSet, LakeAPIView, ContentListView, \
    ContentCreateView, ContentDetailView, MyContentListView, ContentUpdateView, SmartContentListView, CommentCreateView

app_name = SocialConfig.name


router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'comment', CommentViewSet, basename='comment')
urlpatterns = [path('main/', index, name='main'),
               path('like/', LakeAPIView.as_view(), name='like'),
               # path('content_simple_list/', CustomListView.as_view(), name='content_simple_list'),
               path('content_simple_list/', ContentListView.as_view(), name='content_simple_list'),
               path('content_my_list/', MyContentListView.as_view(), name='my_content_list'),
               path('content_smart_list/', SmartContentListView.as_view(), name='content_smart_list'),

               path('comment_create/', CommentCreateView.as_view(), name='comment_create'), # TODO сделать ссылки на всех шаблонах

               path('content_create/', ContentCreateView.as_view(), name='content_create'),
               path('content_update/<int:pk>/', ContentUpdateView.as_view(), name='content_update'),
               path('content_detail/<int:pk>/', ContentDetailView.as_view(), name='content_detail')

               ] + router.urls

