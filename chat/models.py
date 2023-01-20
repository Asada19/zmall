from advertisement.models import Advertisement
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
