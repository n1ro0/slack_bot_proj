from django.shortcuts import render, redirect
from django.views import generic
from . import models
from . import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from urllib.parse import parse_qs

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView


class RegisterCreateView(generic.CreateView):
    template_name = "sign_up.html"
    model = models.SlackBotUser
    form_class = forms.SlackBotUserCreationForm
    success_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/accounts/profile/')
        else:
            return super(RegisterCreateView, self).get(self, request, args, kwargs)


class MyLoginView(LoginView):
    template_name = 'login.html'


class ProfileView(generic.View):
    def get(self, request, *args, **kwargs):
        profile = models.UserProfile.objects.filter(user_id=request.user.id).first()
        if not profile:
            profile = models.UserProfile.objects.create(user_id=request.user.id)
        return render(request, 'profile.html', context={'profile': profile})


class ProfileUpdateView(generic.UpdateView):
    template_name = 'profile_update.html'
    model = models.UserProfile
    form_class = forms.UserProfileCreationForm
    success_url = '/accounts/profile'

    def get_object(self):
        profile = models.UserProfile.objects.filter(user_id=self.request.user.id).first()
        return models.UserProfile.objects.get(pk=profile.id)