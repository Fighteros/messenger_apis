from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ChatHistory, Message
from .serializers import UserSerializer, ChatHistorySerializer, MessageSerializer


# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChatHistoryList(generics.ListCreateAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['last_message'] = Message.objects.last()
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# add @csrf_exempt if csrf problems happend to make this view free of csrf
# @csrf_exempt
# def list_messages(request, sender=None, receiver=None):
#     """
#     all required messages, or create a new message.
#     """
#     if request.method == 'GET':
#         serializer = MessageSerializer(data=Message.objects.filter(sender=sender, receiver=receiver), many=True,
#                                        context={'request': request})
#         print(serializer.is_valid())
#         print(serializer.data)
#         serializer.is_valid()
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         # working!
#         if request.user.is_authenticated:
#             if request.user.id == sender:
#                 data = JSONParser().parse(request)
#                 data['last_message'] = Message.objects.last().message
#                 serializer = MessageSerializer(data=data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return JsonResponse(serializer.data, status=201)
#                 return JsonResponse(serializer.errors, status=400)
#             return JsonResponse({"error": "this user isn't allowed to do this"}, safe=False)
#         return JsonResponse({"error": "this user isn't authenticated"}, safe=False)
