from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','subject','sender','recipient','message','is_read']
    