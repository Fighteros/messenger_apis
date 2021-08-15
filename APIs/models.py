from time import timezone

from django.db import models


# Create your models here.
class Chat(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, blank=False)
    chat_id = models.IntegerField(blank=False, unique=True)

    def __str__(self):
        return str(self.id)


class ChatHistory(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    sender_id = models.IntegerField(blank=False, unique=True)
    receiver_id = models.IntegerField(blank=False, unique=True)
    last_message = models.CharField(blank=True, max_length=250)
    message = models.CharField(blank=False, max_length=350)
    sent_date = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)