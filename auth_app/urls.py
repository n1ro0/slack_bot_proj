from . import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view()),
    url(r'^profile/update/$', views.ProfileUpdateView.as_view()),
    url(r'^register/$', views.RegisterCreateView.as_view()),
    url(r'^login/$', views.MyLoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout")
]