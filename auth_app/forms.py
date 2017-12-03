from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SlackBotUserCreationForm(UserCreationForm):
    class Meta:
        model = models.SlackBotUser
        fields = ('username', 'password1', 'password2')


class UserProfileCreationForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ('user',)

