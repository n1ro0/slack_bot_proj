from . import models
from celery import shared_task


@shared_task
def save_bot_connection(message):
    try:
        models.BotConnection.objects.get_or_create(admin_id=message['admin_id'],
                                               access_token=message['access_token'],
                                               team_id=message['team_id'],
                                               channel_id=message['channel_id'],
                                               incoming_webhook_url=message['incoming_webhook_url']
                                               )
    except:
        print("Team {} is already registered.".format(message['team_id']))


@shared_task
def save_message(message):
    try:
        models.BotMessage.objects.get_or_create(bot_connection_id=message['bot_connection_id'],
                                                sender_id=message['sender_id'],
                                                ts=message['ts'],
                                                text=message['text']
                                                )
    except:
        print("Message {} exists.".format(message['ts']))


@shared_task
def save_reply(reply):
    try:
        models.BotReply.objects.get_or_create(bot_message_id=reply['bot_message_id'],
                                              sender_id=reply['sender_id'],
                                              ts=reply['ts'],
                                              text=reply['text']
                                              )
    except:
        print("Reply {} exists.".format(reply['ts']))