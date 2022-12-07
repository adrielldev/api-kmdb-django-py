from datetime import date, datetime
from rest_framework import serializers


from users.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=127)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(format="%Y-%m-%d")
    bio = serializers.CharField(default="null")
    is_critic = serializers.BooleanField(default=False)
    updated_at = serializers.DateField(default=date.today())


    def create(self,validated_data:dict):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

