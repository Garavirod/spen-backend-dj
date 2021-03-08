# third patty apps
from rest_framework import serializers

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.CharField()