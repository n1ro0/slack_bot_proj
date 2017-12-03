from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.IndexTemplateView.as_view()),
    url(r'^bot/oauth/$', views.OauthView.as_view()),
    url(r'^bot/connections/$', views.BotConnectionsView.as_view()),
    url(r'^bot/connections/(?P<pk>\d+)/$', views.BotConnectionUpdateView.as_view()),
    url(r'^bot/connections/(?P<pk>\d+)/messages/$', views.BotConnectionMessagesView.as_view()),
    url(r'^bot/connections/messages/(?P<pk>\d+)/replies/$', views.BotMessageRepliesView.as_view()),
    url(r'^bot/ask/$', views.AskView.as_view()),
    url(r'^bot/action/reply/$', views.ReplyActionView.as_view())

]