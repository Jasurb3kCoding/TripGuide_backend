import datetime
from hashlib import md5
from uuid import uuid4

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers, models, permissions
from config import settings


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'success': True,
            'email': serializer.data.get('email')
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


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


@api_view(['POST'])
def user_verify(request):
    serializer = serializers.UserVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get('email')
        code = request.data.get('code')
        hash_code = md5(code.encode()).hexdigest()
        obj = models.UserVerificationCode.objects.filter(email=email, code=hash_code).last()
        if obj and obj.is_valid():
            user = obj.user
            user.is_verified = True
            user.save()
            refresh = serializers.MyTokenObtainPairSerializer().get_token(user)
            data = {
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = serializer.errors
        data['success'] = False
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_recovery_link(request):
    serializer = serializers.UserPassowordRecoveryLinkSerializer(data=request.data)
    if serializer.is_valid():
        try:
            email = request.data.get('email')
            user = models.User.objects.get(email=email)
            uid = uuid4()
            link = f'{settings.FRONTEND_URL}reset-password/{uid}'
            obj = models.PasswordRecoveryLink.objects.create(email=email, user=user,
                                                             valid_to=timezone.now() + datetime.timedelta(
                                                                 seconds=settings.PASSWORD_RECOVERY_LINK_LIFETIME),
                                                             link=link,
                                                             uid=uid)
            send_mail(subject='Your password reset link',
                      message=f'Hi {user.first_name},\n\nThere was a request to change your password!\n\nIf you did not make this request then please ignore this email.\n\nOtherwise, please click this link to change your password: {obj.link}',
                      from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ])
            return Response({'success': True, 'message': 'We\'ve send password recovery link to your email'},
                            status=status.HTTP_200_OK)

        except models.User.DoesNotExist:
            print('user not found')
            return Response({'success': False, 'message': 'No active account found with the given email address'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        data = serializer.errors
        data['success'] = False
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_recovery(request):
    serializer = serializers.PasswordRecoverySerializer(data=request.data)
    if serializer.is_valid():
        uid = request.data.get('uid')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        obj = models.PasswordRecoveryLink.objects.filter(uid=uid).last()
        if obj and not obj.expired:
            user = obj.user
            if password1 == password2:
                user.set_password(password1)
                user.save()
                obj.expired = True
                obj.save()
                return Response({'success': True, 'message': 'Your password changed successfully!'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'Password didn\'t match'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': False, 'message': 'This link was expired please try again with another link'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        data = serializer.errors
        data['success'] = False
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
