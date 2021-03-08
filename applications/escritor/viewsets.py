""" Third party apps """
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
""" Serializers """
from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer
)
""" Models """
from .models import Usuarios
""" django """
from django.shortcuts import get_object_or_404


class RegisterUserViewset(viewsets.ViewSet):

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

        
class LoginUserViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'])
    def login(self,request):
        deserialized_data = LoginUserSerializer(data=data.request)
        deserialized_data.is_valid(raise_exception=True)
        return Response({'ok':'hola'})   