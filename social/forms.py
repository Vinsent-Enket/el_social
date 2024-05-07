from django import forms

from social.models import Content, Comment


class ContentForm(forms.ModelForm):
    """"
    TODO Добавить проверку на уровень подписки можно тут?
    """
    class Meta:
        model = Content
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    """комменты не работают, так как для создания нужно в кнопке передавать id поста к которому присоеденяется комментарий"""

    class Meta:
        model = Comment
        fields = ('author',)


