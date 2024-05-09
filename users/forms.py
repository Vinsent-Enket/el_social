from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User, Subscription


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('telephone', 'password1', 'password2',)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('telephone', 'first_name', 'last_name', 'email', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'
