from django.contrib import admin
from . import models


admin.site.register((models.BotConnection, models.BotMessage, models.BotReply))
