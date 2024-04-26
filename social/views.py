from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Content, Like, Comment
from social.permissions import IsProprietor
from social.serializers import ContentSerializer, CommentsSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


# Create your views here.

def index(request):
    return render(request, 'social/index.html')


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LakeAPIView(APIView):
    def post(self, *args, **kwargs):
        content_id = self.request.data.get('content_id')
        user = self.request.user
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            message = f'Такого поста не существует'
            code = HTTP_404_NOT_FOUND
        else:
            if Like.objects.filter(author=user, content=content).exists():
                Like.objects.filter(author=user, content=content).delete()
                message = 'Удалено'
                code = HTTP_204_NO_CONTENT
            else:
                Like.objects.create(author=user, content=content).save()
                message = 'Добавлено'
                code = HTTP_201_CREATED

        return Response({'message': message}, status=code)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


    def get_queryset(self):
        queryset = Comment.objects.all()
        content_filter = self.request.query_params.get('content_filter')
        if content_filter:
            queryset = queryset.filter(content_id=content_filter)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
