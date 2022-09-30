from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
import datetime

from rest_framework.permissions import IsAuthenticated

from account import serializers, models, permissions
from config.settings import PASSWORD_RECOVERY_CODE_LIFETIME


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.verified.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
    lookup_field = 'id'


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class UserSettingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.UserSetting.objects.all()
    serializer_class = serializers.UserSettingSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.kwargs.get('id'))
        return obj


class LanguageListView(generics.ListAPIView):
    queryset = models.LanguageSetting.objects.all()
    serializer_class = serializers.LanguageSerializer


class PasswordRecoveryCodeView(generics.CreateAPIView):
    queryset = models.PasswordRecoveryCode.objects.all()
    serializer_class = serializers.PasswordRecoveryCodeSerializer

    def perform_create(self, serializer):
        serializer.save(valid_to=timezone.now() + datetime.timedelta(seconds=PASSWORD_RECOVERY_CODE_LIFETIME))


@api_view(['GET'])
def password_recovery_code_detail(request):
    email = request.data.get('email')
    code = request.data.get('code')
    _code = make_password(code)
    print(_code)
    qs = models.PasswordRecoveryCode.objects.filter(email=email, code=_code).last()
    if qs.is_valid():
        pass
    pass
