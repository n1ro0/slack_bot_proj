from django.db import models
from django.contrib.auth import models as auth_models


class SlackBotUser(auth_models.AbstractUser):
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    name = models.CharField(max_length=30, default='name')
    surname = models.CharField(max_length=30, default='surname')
    user = models.ForeignKey(SlackBotUser)
    photo = models.ImageField(default="profile_photos/default.png", upload_to="profile_photos")

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

