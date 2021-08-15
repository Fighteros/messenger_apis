from django.contrib import admin

# Register your models here.
from APIs.models import Chat, ChatHistory

admin.site.register(Chat)
admin.site.register(ChatHistory)