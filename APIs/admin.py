from django.contrib import admin

# Register your models here.
from APIs.models import Message, ChatHistory, Chat

admin.site.register(Chat)
admin.site.register(ChatHistory)
admin.site.register(Message)
