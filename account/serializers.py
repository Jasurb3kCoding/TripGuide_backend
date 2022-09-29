from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from account import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def update(self, instance, validated_data):
        print(validated_data)
        fields = list(super().get_fields().keys())
        [fields.remove(item) for item in
         ['email', 'first_name', 'last_name', 'profile_photo', 'background_photo']]
        print(fields)
        for field in fields:
            if field in validated_data:
                validated_data.pop(field)
                print(field)
        user = super().update(instance, validated_data)
        return user

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class MyTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
            "is_verifed": True
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        if self.user.is_verified == False:
            self.user = None

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSetting
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LanguageSetting
        fields = '__all__'
