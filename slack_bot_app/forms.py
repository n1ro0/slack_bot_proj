from . import models
from django import forms


class BotConnectionForm(forms.ModelForm):
    class Meta:
        model = models.BotConnection
        exclude = ('admin', 'incoming_webhook_url')