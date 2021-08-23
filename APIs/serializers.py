from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from APIs.models import ChatHistory, Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatHistorySerializer(WritableNestedModelSerializer):
    chat = ChatSerializer()
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    last_message = serializers.CharField(allow_null=True)

    class Meta:
        model = ChatHistory
        fields = '__all__'


class MessageSerializer(WritableNestedModelSerializer):
    chat_history = serializers.SlugRelatedField(many=False, slug_field='chat_id', queryset=ChatHistory.objects.all())

    class Meta:
        model = Message
        fields = '__all__'


# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
#     receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
#
#     class Meta:
#         model = Message
#         fields = ('sender', 'receiver', 'last_message', 'message', 'timestamp',)
