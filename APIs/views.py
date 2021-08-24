from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ChatHistory, Message, UserProfile
from .serializers import UserSerializer, ChatHistorySerializer, MessageSerializer, UserProfileSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        profile_img = request.data['profile_img']
        request.data['user'] = User.objects.filter(username=request.data['user']).first().pk
        serializer = ""
        try:
            serializer = UserProfileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return JsonResponse({'Error Message': 'User has a profile already'})


class ChatHistoryList(generics.ListCreateAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['last_message'] = Message.objects.last()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# list all Messages
class MessageList(generics.ListCreateAPIView):
    """
    List all messages or create new Messages
    get all messages or get with seen
    paginate messages for both
    """
    serializer_class = MessageSerializer

    # removed duplication for steps in the condition
    def pag_messages(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MessageSerializer(data=page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(data=queryset, many=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    # PAGINATE MESSAGES
    def get(self, request, *args, **kwargs):
        data = self.request.query_params
        if data.get('chat_id'):
            queryset = Message.objects.filter(chat_history__chat__chat_id__contains=data['chat_id'], isRead=False)
            for message in queryset:
                message.isRead = True
                message.save()
            return self.pag_messages(queryset)
        else:
            queryset = Message.objects.all()
            return self.pag_messages(queryset)
