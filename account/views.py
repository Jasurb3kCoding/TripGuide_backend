from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from account import serializers, models, permissions


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
    lookup_field = 'id'


class UserSettingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.UserSetting.objects.all()
    serializer_class = serializers.UserSettingSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.kwargs.get('id'))
        return obj


class LanguageListView(generics.ListAPIView):
    queryset = models.LanguageSetting.objects.all()
    serializer_class = serializers.LanguageSerializer


class TimeZoneListView(generics.ListAPIView):
    queryset = models.TimeZoneSetting.objects.all()
    serializer_class = serializers.TimeZoneSerializer
