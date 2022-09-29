from account import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def update(self, instance, validated_data):
        fields = list(super().get_fields().keys())
        [fields.remove(item) for item in
         ['email', 'first_name', 'last_name', 'profile_photo', 'background_photo']]
        print(fields)
        for field in fields:
            if field in validated_data:
                validated_data.pop(field)
                print(field)
        user = super().update(instance, validated_data)
        print(user)
        return user


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSetting
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LanguageSetting
        fields = '__all__'


class TimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeZoneSetting
        fields = '__all__'
