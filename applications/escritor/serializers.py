# third patty apps
from rest_framework import serializers
# models
from .models import Usuarios

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.CharField()

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class AutorSerializerData(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ('pk','username','aboutme','email')


