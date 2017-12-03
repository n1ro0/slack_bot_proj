from django.contrib import admin
from . import models


admin.site.register((models.SlackBotUser, models.UserProfile))