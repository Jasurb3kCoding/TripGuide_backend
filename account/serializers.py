from account import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = super().create(validated_data)
    #     user.set_password(password)
    #     user.is_active = True
    #     user.save()
    #     return user


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'phone_number', ]

    def update(self, instance, validated_data):
        print(validated_data)
        user = super().update(instance, validated_data)
        user.is_active = True
        user.save()
        return user
