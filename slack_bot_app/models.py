from django.db import models
from auth_app import models as auth_models


class BotConnection(models.Model):
    admin = models.ForeignKey(auth_models.SlackBotUser)
    access_token = models.CharField(max_length=100)
    channel_id = models.CharField(max_length=30)
    team_id = models.CharField(max_length=30, unique=True)
    incoming_webhook_url = models.CharField(max_length=100)
    moderators = models.ManyToManyField(auth_models.SlackBotUser, related_name='bot_connections')

    def __str__(self):
        return self.team_id


class BotMessage(models.Model):
    sender_id = models.CharField(max_length=50)
    bot_connection = models.ForeignKey(BotConnection)
    ts = models.CharField(max_length=50, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.ts


class BotReply(models.Model):
    bot_message = models.ForeignKey(BotMessage)
    sender_id = models.CharField(max_length=30)
    ts = models.CharField(max_length=50, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.id


