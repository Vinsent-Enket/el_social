from rest_framework import serializers, status
from rest_framework.response import Response

from social.models import Content, Like, Comment


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['author']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        #fields = '__all__'
        exclude = ['author']

    # def create(self, validated_data):
    #     flag = self.context['request'].data['flag']
    #
    #     print(flag)
    #     try:
    #         if flag == 'create':
    #             validated_data['author'] = self.context['request'].user
    #             instance = Comment.objects.create(**validated_data)
    #             instance.save()
    #             return instance
    #         elif flag == 'list':
    #             filter_kwargs = {"content": self.context['request'].data['content']}
    #             print(filter_kwargs['content'])
    #             queryset = Comment.objects.filter(**filter_kwargs)
    #             return Response(CommentsSerializer(queryset, many=True).data)
    #
    #     except KeyError:
    #         raise serializers.ValidationError('Нет флага, укажите "create"/"list"')


class ContentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    your_likes = serializers.SerializerMethodField()

    def get_likes(self, instance):
        # не работает related_name
        return instance.like_set.all().count()
        # return instance.post_likes.all().count()

    def get_comments(self, instance):
        return instance.comment_set.all().count()

    def get_your_likes(self, instance):
        return instance.like_set.filter(author=self.context['request'].user).exists()

    class Meta:
        model = Content
        exclude = ['author']
