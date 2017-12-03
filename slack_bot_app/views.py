from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from urllib.parse import parse_qs
from . import models, forms, tasks
from auth_app import models as auth_models
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from slackclient import SlackClient


class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'


class BotConnectionsView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['bot_connections'] = models.BotConnection.objects.filter(admin_id=request.user.id)
        context['users'] = auth_models.SlackBotUser.objects.exclude(id=request.user.id)
        context['moderated_connections'] = get_object_or_404(auth_models.SlackBotUser.objects.prefetch_related('bot_connections'), id=request.user.id).bot_connections.all()
        context['client_id'] = settings.SLACK_CLIENT_ID
        context['scope'] = settings.SLACK_SCOPE
        context['redirect_uri'] = settings.SLACK_OAUTH_REDIRECT_URL
        context['state'] = settings.SLACK_STATE
        return render(request, 'bot_settings.html', context=context)

    def post(self, request, *args, **kwargs):
        bot_connection_id = request.POST['id']
        usernames = request.POST.getlist('usernames[]')
        print(usernames)
        moderators = get_object_or_404(models.BotConnection.objects, id=bot_connection_id).moderators
        for username in usernames:
            user = get_object_or_404(auth_models.SlackBotUser.objects, username=username)
            moderators.add(user)
        return redirect('/bot/connections/')



class BotConnectionUpdateView(generic.UpdateView):
    template_name = 'bot_setting_update.html'
    model = models.BotConnection
    form_class = forms.BotConnectionForm
    success_url = '/bot/connections/'


class BotConnectionMessagesView(LoginRequiredMixin, generic.DetailView):
    template_name = 'bot_connection_asks.html'
    model = models.BotConnection
    context_object_name = 'bot_connection'

    def get_context_data(self, **kwargs):
        context = super(BotConnectionMessagesView, self).get_context_data(**kwargs)
        context['bot_messages'] = models.BotMessage.objects.filter(bot_connection_id=self.kwargs['pk'])
        return context


class BotMessageRepliesView(LoginRequiredMixin, generic.DetailView):
    template_name = 'bot_messages_replies.html'
    model = models.BotMessage
    context_object_name = 'bot_message'

    def get_context_data(self, **kwargs):
        context = super(BotMessageRepliesView, self).get_context_data(**kwargs)
        context['bot_replies'] = models.BotReply.objects.filter(bot_message_id=self.kwargs['pk'])
        return context


class OauthView(generic.View):
    def get(self, request, *args, **kwargs):
        qs = parse_qs(request.environ['QUERY_STRING'])
        code = qs.get('code', [''])[0]
        state = qs.get('state', [''])[0]
        if state != settings.SLACK_STATE:
            return HttpResponse("Wrong state!")
        response = requests.get('https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}&redirect_uri={}'.format(
            settings.SLACK_CLIENT_ID, settings.SLACK_CLIENT_SECRET, code, settings.SLACK_OAUTH_REDIRECT_URL
        ))
        content = response.json()
        user_id = request.user.id
        access_token = content['access_token']
        team_id = content['team_id']
        channel_id = content['incoming_webhook']['channel_id']
        incoming_webhook_url = content['incoming_webhook']['url']
        tasks.save_bot_connection.delay({
            'admin_id': user_id,
            'access_token': access_token,
            'team_id': team_id,
            'channel_id': channel_id,
            'incoming_webhook_url': incoming_webhook_url
        })
        return redirect('/bot/connections/')


@method_decorator(csrf_exempt, 'dispatch')
class AskView(generic.View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        token = request.POST['token']
        if token != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse(status='403')
        text = request.POST['text']
        user_id = request.POST['user_id']
        sender = request.POST['user_name']
        team_id = request.POST['team_id']
        bot_connection = get_object_or_404(models.BotConnection.objects, team_id=team_id)
        sc = SlackClient(bot_connection.access_token)
        resp = sc.api_call(
            "chat.postMessage",
            channel=bot_connection.channel_id,
            text='User @' + sender + ' needs to leave: ' + text
        )
        text = resp['message']['text']
        ts = resp['message']['ts']
        tasks.save_message.delay({
            'bot_connection_id': bot_connection.id,
            'sender_id': user_id,
            'ts': ts,
            'text': text
        })
        return HttpResponse('Successfully sent!')


@method_decorator(csrf_exempt, 'dispatch')
class ReplyActionView(generic.View):
    def post(self, request, *args, **kwargs):
        reply_data = json.loads(request.body.decode())
        token = reply_data.get('token', None)
        if token != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse(status='403')
        thread_ts = reply_data.get('event', {}).get('thread_ts', None)
        if thread_ts is None:
            return HttpResponse()
        text = reply_data.get('event', {}).get('text', '')
        user = reply_data.get('event', {}).get('user', '')
        ts = reply_data.get('event', {}).get('ts', '')
        message = get_object_or_404(models.BotMessage.objects, ts=thread_ts)
        bot_connection = get_object_or_404(models.BotConnection.objects, id=message.bot_connection_id)
        tasks.save_reply.delay({
            'bot_message_id': message.id,
            'sender_id': user,
            'ts': ts,
            'text': text
        })
        sc = SlackClient(bot_connection.access_token)
        sc.api_call(
            "chat.postMessage",
            channel=message.sender_id,
            text=message.text + ' ---->>> ' + text
        )
        return HttpResponse()


