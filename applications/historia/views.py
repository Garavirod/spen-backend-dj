# Dajngo
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
# Model
from .models import Historias, Valoraciones
from applications.escritor.models import Usuarios
# Serializers
from .serializers import (
    NewStorySerializer,
    GetDataHistoriasSerializer,  
    HistoriasBriefSerializer,
    AutorProfileSerializer,  
    MyProfileSerializer,
    BriefStoriesSerializer,
    FullContentSerializer,
    StoryCommentsSerializer,
    ValoracionSerializer,
    AlreadyValuedSrializer,
)
# Custom permissons
from .permissons import IsOwner

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
        Muestra la información resumida de todas las 
        historias que han sido marcadas con estatus 
        terminado (True)
    """
    serializer_class = BriefStoriesSerializer
    # Todas las historias que ya han sido finalizadas
    queryset = Historias.objects.filter(status=True)

class AuthorStoriesAPIView(ListAPIView):
    """ 
        Muestra la iformación resumiada de las
        historias terminadas de un autor en 
        especifico.
    """
    # ligamos el serializador
    serializer_class = BriefStoriesSerializer        
    # Override
    def get_queryset(self):
        # Obtenemos el autor por pk           
        autor = get_object_or_404(Usuarios,pk=self.kwargs['pk'])
        # filtramos las historias del autor              
        queryset = Historias.objects.filter(status=True, autor=autor)            
        return queryset

class MyStoriesAPIView(ListAPIView):
    """ 
        Muestra la iformación resumiada de las
        historias terminadas del propio autor,
        es necesario mandar el token.
    """
    
    # tipo de autenticación por token mandado por cabecera Authorization: Token <_token_>
    authentication_classes = (TokenAuthentication,) 
    permission_classes = [
        IsAuthenticated, # Verificamos la autenticación del usuario 
    ] 

    # ligamos el serializador
    serializer_class = BriefStoriesSerializer        
    # Override
    def get_queryset(self):
        # Obtenemos el autor por pk           
        autor = get_object_or_404(Usuarios,pk=self.kwargs['pk'])
        # filtramos las historias del autor              
        queryset = Historias.objects.filter(autor=autor)            
        return queryset


class ReadingModeStoryAPIView(RetrieveAPIView):
    """ Recupera una historia junto con su contenido por PK  """
    # Ligamos seriaizador
    serializer_class = FullContentSerializer
    # override
    queryset = Historias.objects.filter()

class WrittingModeStoryView(RetrieveUpdateDestroyAPIView):
    """  
        Recupera una historia en modo edición y la actualiza 
        o elimina si el usuario es autor de la historia.        
        Se envia token en la cabecera para autenticar al usuario.
        Puede activarse por los verbos HTTP PUT, GET, DELETE
    """
    # tipo de autenticación por token mandado por cabecera Authorization: Token <_token_>
    authentication_classes = (TokenAuthentication,)
    # verificamos que el usuario esté autenticado y que sea el propietraio de la historia 
    permission_classes = [IsAuthenticated & IsOwner]     
    # Ligamos el serializador
    serializer_class = FullContentSerializer

    queryset = Historias.objects.all()


class StoryCommentsView(ListAPIView):
    """ Muestra todos los comentarios de una historia 
        en especifico basado en sus PK
    """

    # Ligamos serializador
    serializer_class = StoryCommentsSerializer

    # Override
    def get_queryset(self):
        # resuperamos histria por pk
        historia = get_object_or_404(Historias, pk=self.kwargs['storyPk'])
        queryset = historia.comentarios_set.all()
        return queryset

class AddValoracionView(CreateAPIView):
    """ 
        Captura los atributos escenciales
        para agregar una valoracion a una historia en espcifico
        Es necesario enviar el token por cabecera.  
    """

    # Tipo de autenticación por token mandado por cabecera Authorization: Token <_token_>
    authentication_classes = (TokenAuthentication,)
    # verificamos que el usuario esté autenticado y que sea el propietraio de la historia 
    permission_classes = [IsAuthenticated]     
    # Ligamos el serializador
    serializer_class = ValoracionSerializer

    # Override
    def create(self, request):
        try:
            # Deserializamos la infromación
            deserialized_data = ValoracionSerializer(data=request.data)
            # validamos la data deserializada
            deserialized_data.is_valid(raise_exception=True)
            # Ususario que resalizo la petición
            user = request.user
            # Historia que se valorará
            historia = Historias.objects.get(pk=deserialized_data.data['historia_valoracion'])
            # Creamos una valoración
            valoracion = Valoraciones.objects.create(
                puntaje=deserialized_data.data['puntaje'],
                autor_valoracion=user,
                historia_valoracion=historia
            )
            # Guaradamos cambios en la BDD
            valoracion.save()
            # Valoración creada con exito            
            return Response({'message':'Valoración agregada'}, status=status.HTTP_201_CREATED)
        except:
            # La valoración no pudo ser creada
            return Response(
                {'message':'La valoración no fupeagregada'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlreadyValuedView(APIView):
      
    # Override            
    def get(self,request):
        try:
            # Valoración por defecto
            is_valued_mess = { 'is_valued' : False }
            # Casteamos la pk's
            pk_user = int(self.request.query_params.get('pkUser'))
            pk_historia = int(self.request.query_params.get('pkHistoria'))

            # Buscamos si el usuario ya valoro esa historia
            is_valued = Valoraciones.objects.filter(
                autor_valoracion__id=pk_user,
                historia_valoracion__id=pk_historia
            )

            # si hubo un registro
            if is_valued:
                is_valued_mess['is_valued'] = True
            # response 
            return Response(is_valued_mess, status=status.HTTP_202_ACCEPTED)            
        except:           
            return Response(
                    {'message':'Error al verifcar la valoración'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            