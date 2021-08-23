from django.contrib.auth.models import User
from django.db import models


# ForeignKey means A Many-to-one relationship
class Chat(models.Model):
    chat_id = models.CharField(max_length=255, primary_key=True)

    class Meta:
        ordering = ["chat_id"]

    def __str__(self):
        return self.chat_id


class ChatHistory(models.Model):
    # each ChatHistory belongs to a Chat and only one chat
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat")
    # each ChatHistory has only one sender and receiver
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    last_message = models.CharField(max_length=255, null=True)
    # auto_now each time .save() auto_now_add the first time of creation only
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chat']

    def __str__(self):
        return self.chat.chat_id


class Message(models.Model):
    # each Message belongs to a ChatHistory
    chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name="chat_history")
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
