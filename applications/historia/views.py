# Dajngo
from django.shortcuts import render
# third party apps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
# Model
from .models import Historias
# Serializers
from .serializers import (
    NewStorySerializer,
    GetDataHistoriasSerializer,
)

class RegisterNewStoryAPIView(CreateAPIView):
    """ 
        Obtiene  los datos escenciales para la 
        creación de una instancia del modelo Historia        
    """
    # Verifivamos la autenticación del usuario 
    # tipo de autenticación por token mandado por cabecera Authorization: Token <_token_>
    authentication_classes = (TokenAuthentication,) 
    permission_classes = [
        IsAuthenticated, #if is authenticated     
    ] 

    # Ligamos serializaor
    serializer_class = NewStorySerializer

    # Override
    def create(self,request):
        # deserializado de información
        deserialized_data = NewStorySerializer(data=request.data)
        # validamos deserialización
        deserialized_data.is_valid(raise_exception=True)
        try:
            # recuperamos al usuario que hace la petición
            user = request.user            
            # creamos la instancía Historia
            historia = Historias(
                titulo=deserialized_data.data['titulo'],
                narrativa=deserialized_data.data['narrativa'],
                genero=deserialized_data.data['genero'],
                autor=user # ligamos al autor con la historia creada
            )
            # guaradamos la historia en BDD
            historia.save()            
            # historia creada con exito
            return Response({'message':'Historia creada con éxito'}, status=status.HTTP_201_CREATED)
        except:
            # Error al crear la historia
            return Response({'message':'Error al crear la historia'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllPublishedStoriesAPIView(ListAPIView):
    """ 
        Muestra la infromación resumida todas las 
        historias que han sido marcadas con estatus 
        terminado (True)
    """
    serializer_class = GetDataHistoriasSerializer
    queryset = Historias.objects.filter(status=True)