from django import forms

from social.models import Content, Comment


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


