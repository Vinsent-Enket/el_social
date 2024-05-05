from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import MultipleObjectMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from social.forms import ContentForm, CommentForm
from social.models import Content, Like, Comment
from social.permissions import IsProprietor
from social.serializers import ContentSerializer, CommentsSerializer, SimpleContentSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.renderers import TemplateHTMLRenderer

from users.models import Subscription
from users.permission import IsModerator


# Create your views here.

def index(request):
    return render(request, 'social/index.html')


class ContentListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'social/content_list.html'
    context_object_name = 'content_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_list = Comment.objects.all()
        context['comments_list'] = comments_list
        likes_list = Like.objects.filter(author=self.request.user)
        context['likes_list'] = likes_list
        return context

    def get_queryset(self):
        user = self.request.user
        subscribe = Subscription.objects.filter(proprietor=user).values_list('author', flat=True)
        print(subscribe)
        queryset = Content.objects.filter(Q(author__in=subscribe))
        return queryset


class SmartContentListView(ContentListView):
    def get_queryset(self):
        user = self.request.user
        subscribe = Subscription.objects.filter(proprietor=user).values_list('author', flat=True)
        queryset = Content.objects.exclude(author__in=subscribe)
        return queryset


class MyContentListView(LoginRequiredMixin, ListView): # TODO наследуйтесь от ContentListView
    model = Content
    template_name = 'social/content_my_list.html'
    context_object_name = 'content_list'

    def get_queryset(self):
        queryset = Content.objects.filter(author=self.request.user)
        return queryset


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('social:content_simple_list')  # TODO не забыть отключить поле владельца


class ContentDetailView(LoginRequiredMixin, DetailView):
    model = Content
    context_object_name = 'content'
    template_name = 'social/content_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_list = Comment.objects.all()  # TODO сделать фильтрацию
        context['comments_list'] = comments_list
        return context


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('social:my_content_list')

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user != self.object.author:
            reverse_lazy('social:content_simple_list')
            print('это не твой продукт брысь')
            form.add_error(None, 'это не твой продукт брысь')
            return super().form_invalid(form)
        self.object.save()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('social:content_simple_list')  # TODO доделать CRUD
    template_name = 'social/comments/comment_form.html'


class ContentViewSet(viewsets.ModelViewSet):
    # TODO отключить ли ;лист;? да отключить нахрен, а лучше разбить на отдельные классы APIList и APIDetail и тд

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.renderer_classes = [TemplateHTMLRenderer]
            self.template_name = 'social/content_list.html'
            # self.serializer_class = SimpleContentSerializer
            self.permission_classes = [AllowAny]
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

    # def get(self):
    #     return Response({"content_list": Content.objects.all()})

    def get(self, request):

        content_list = Content.objects.all()
        context = {'content_list': content_list}
        return Response(context)

    def get_queryset(self):
        queryset = Content.objects.all()
        content_filter = self.request.query_params.get('selection')
        print(content_filter)
        if self.action == 'list':  # TODO сделать все три видов лент, наверное отдельными классами
            if content_filter:
                ids_str = ','.join([str(id) for id in content_filter])
                # TODO сделать шаблоны для всех запросов в отдельном файле
                # Создание queryset из записей, ID которых есть в списке
                queryset = Content.objects.filter(
                    author__id__in=ids_str.split(','))  # позволяет получить посты только с определенными авторами
                # queryset = queryset.filter(Q(pk__in=ids_str.split(',')))  # NOTE разобраться позже
            # else:
            #     queryset = queryset.filter(level__lte=self.request.user.level)

        return queryset


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
