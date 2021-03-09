# Third party apps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView
)
# Serializers
from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer
)
# Models
from .models import Usuarios
# Django
from django.shortcuts import render
from django.contrib.auth.hashers import check_password

# Create your views here.
class RegisterNewUserAPIView(CreateAPIView):
    """ 
        Obtiene los datos escenciales del usuario para crear 
        una caunta o registrarse en el sistema.
    """ 
    # Ligamos el serializador
    serializer_class = RegisterUserSerializer

    def _registerNewUser(self, username, email, password, gender):
        """  
            Método privado que se encarga de crear un usuario en la app 
            de django de acuerdo al manager customizado
            para la gestion de usuarios de django.
        """
        try:
            # Llama al metodo manager que se encarga de gestionsr los usuer en Django
            user = Usuarios.objects.create_user(                
                email,
                password,
                # campos extra
                username=username,
                gender=gender                
            )
            # Creamos el token
            token = Token.objects.create(user=user)
            return {'ok':True, 'token':token.key} # retornamos el token.key y una bandera True
        except:
            return {'ok':False, 'message':'Error al registrar usuario'}

    # Override
    def create(self, request):                       
        # deserializamos la infromación del usuario
        deserialized_data = RegisterUserSerializer(data=request.data)
        # validamos la data deserializda
        deserialized_data.is_valid(raise_exception=True)               
        # verificamos existencia o creamos nuevo usuario
        try:
            user = Usuarios.objects.get(email=deserialized_data.data['email'])           
            if user:
                content = {'ok':False, 'message':'El usuario ya existe'}
                return Response(content, status=status.HTTP_409_CONFLICT)
        except:
            # llamamos al metodo en cargado de ejecyura el proceo de crear nuevos usuarios
            created_content = self._registerNewUser( # retorna la respuesta segun la creación del usuario
                deserialized_data.data['username'],
                deserialized_data.data['email'],
                deserialized_data.data['password'],
                deserialized_data.data['gender'],
            )
            if created_content['ok']: # verificamos la bandera del proceso ejecutado
                # Usuario creado con éxito
                return Response(created_content, status=status.HTTP_201_CREATED)
            # Error al crear al usuario
            return Response(created_content ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginUserAPIView(APIView):
    """ 
        Autentica al usuario en el sistema basado en las credenciales:
        - email
        - password
    """
    # Override
    def post(self,request):
        # capturamos los datos
        deserialized_data = LoginUserSerializer(data=request.data)
        # validamos la data deserializada
        deserialized_data.is_valid(raise_exception=True)
        # verificamos la existencia del usuario
        try:
            # Recuperamos usuario
            user = Usuarios.objects.get(email=deserialized_data.data['email'])
            # verificamos password del usuario
            valid_pass = user.check_password(deserialized_data.data['password'])
            if valid_pass:  # si el passowrd fué valido
                # recuperamos el token del usuario
                token = Token.objects.get(user=user)
                # Datos del usuario a retornar
                data_user = {                
                    'email':user.email,
                    'username':user.username,
                    'uid':user.pk,
                    'token':token.key
                }
                return Response(data_user, status=status.HTTP_202_ACCEPTED)
                # Usuario no autorizado
            return Response({'message':'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuarios.DoesNotExist:
            # El usuario no existe
            return Response({'message':'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
           