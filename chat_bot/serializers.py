from rest_framework import serializers
from .models import Message

# chat/serializers.py
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'response', 'timestamp']
        read_only_fields = ['response', 'timestamp']
