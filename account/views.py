from hashlib import md5

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers, models, permissions


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
        serializer.errors['success'] = False
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def iya(request):
#     serializer = serializers.PasswordRecoveryCodeCheckSerializer(data=request.data)
#     if serializer.is_valid():
#         email = request.data.get('email')
#         code = request.data.get('code')
#         hash_code = md5(code.encode()).hexdigest()
#         obj = models.PasswordRecoveryCode.objects.filter(email=email, code=hash_code).last()
#         if obj and obj.is_valid():
#             uid = uuid4()
#             models.PasswordRecoveryHash.objects.create(user=obj.user, hash=uid,
#                                                        valid_to=timezone.now() + datetime.timedelta(
#                                                            seconds=PASSWORD_RECOVERY_HASH_LIFETIME))
#             return Response({'access': uid}, status=status.HTTP_200_OK)
#         else:
#             return Response({'access': None}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
