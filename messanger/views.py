from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from messanger.serializers import MessageSerializer
from .models import Message
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.db.models import Q



class MessegeViewSet(viewsets.ModelViewSet, TokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        if user is None:
            return Response({"Answer": "Invalid request: AnonymousUser"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(sender=user)


    @action(detail=False)
    def unread(self, request,*args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(recipient=request.user,is_read=False)
        if not queryset:
            return Response({"Answer": "You don't have unread messages"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'put','get'])
    def read(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(id=pk, recipient=request.user) | Q(id=pk, sender=request.user))
        if not queryset:
            return Response({"Answer": "You don't have a messages with this ID"}, status=status.HTTP_404_NOT_FOUND)
        queryset.filter(id=pk, recipient=request.user).update(is_read=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(sender=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Answer": "Message has been deleted"}, status=status.HTTP_204_NO_CONTENT)