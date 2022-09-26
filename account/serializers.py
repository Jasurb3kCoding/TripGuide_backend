from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class META:
        model = User
        fields = '__all__'
