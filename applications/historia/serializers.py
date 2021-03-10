# Third partty apps
from rest_framework import serializers, pagination
# Models
from .models import Historias, Comentarios
from applications.escritor.models import Usuarios



class NewStorySerializer(serializers.ModelSerializer):
    """ Serializador para crear una nueva historia """
    class Meta:
        model = Historias
        fields = ['titulo','narrativa','genero']

class BriefStoriesSerializer(serializers.ModelSerializer):
    """ Serializer para recuperar los datos resumidos de una historia """  

    # Inyectamos nuevos campos en el json
    autor_name = serializers.SerializerMethodField()
    class Meta:
        model = Historias
        fields = (
            'pk',
            'titulo',
            'narrativa',
            'genero',
            'sinopsis',
            'created',
            'puntaje',
            'autor_name', # attribute added
            'autor', #FK
        )
        
    def get_autor_name(self,obj):
        """ Retrona como campo el nombre del autor de la instancia obj (Historia) """
        return str(obj.autor.username)


class ReadingStorySerialiser(BriefStoriesSerializer):    
    """ 
        Serializer para recuperar los datos de una historia en su modo lectura.
        La clase hereda de la clase BriefStoriesSerializer y solo se injecta un
        nuevo campo (contenido) en la tupla fields del padre.
    """

    # Inyectamos el campo 'contendio' en la tupla del padre.
    class Meta(BriefStoriesSerializer.Meta):
        BriefStoriesSerializer.Meta.fields += ('contenido',)
        
  

class StoryCommentsSerializer(serializers.ModelSerializer):
    """ Serializer para obtener todos los comentarios de una historia """
    autor_username = serializers.SerializerMethodField()
    class Meta:
        model = Comentarios
        fields = ('contenido','autor_comentario','autor_username',)
    def get_autor_username(self,instance):
        """ Retorna el nombre del usuario de la instancia comentario """
        return str(instance.autor_comentario.username)












""" Not added """

class  HistoriasBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historias
        exclude = ['autor','contenido']

class GetDataHistoriasSerializer(serializers.HyperlinkedModelSerializer):  
    """ Serializer para recuperar los datos resumidos de una historia """  
    # Inyectamos un nuevo campo en la data a través de un método
    autor_name = serializers.SerializerMethodField()
    class Meta:
        model = Historias
        fields = (
            'titulo',
            'narrativa',
            'genero',
            'sinopsis',
            'created',
            'puntaje',
            'autor_name', # attribute added 
            'autor', #FK
        )
        
        # Creamos un link para ver el detalle del autor
        extra_kwargs = {
            'autor':{
                'view_name':'users_app:autor-data',
                'lookup_field' : 'pk'
            }
        }
    
    def get_autor_name(self,obj):
        """ Retrona como campo el nombre del autor de la instancia obj (Historia) """
        return str(obj.autor.username)

class AutorProfileSerializer(serializers.ModelSerializer):
    """ 
        Se encarga de desraializar datos del modelo Usuario
        cons sus respectivas histroias publicadas con el
        status (True).
        Se utiliza cuando un escritor ve el peril de otro
        escritor. 
    """
    # inyectamos un nuevo campo en el modelo
    historias = serializers.SerializerMethodField()
    class Meta:
        model = Usuarios
        fields = (
            'username',
            'email',
            'aboutme',
            'historias', # campo inyectado
        )

    def get_historias(self,obj):        
        # todas las historias que son del autor y que ya son termiandas
        historias = obj.historias_set.filter(status=True)
        # deserializamos ls historias
        deserialized = HistoriasBriefSerializer(historias, many=True)
        # retornamos la data
        return deserialized.data

class MyProfileSerializer(serializers.ModelSerializer):
    """ 
        Se encarga de desraializar datos del modelo Usuario
        con sus respectivas histroias que pueden estar terminadas o no.
        Se utiliza cuando un escritor ve su propia infromación de su peril
        escritor. 
    """
    # inyectamos un nuevo campo en el modelo
    historias = serializers.SerializerMethodField()
    class Meta:
        model = Usuarios
        fields = (
            'username',
            'email',
            'aboutme',
            'historias', # campo inyectado
        )

    def get_historias(self,obj):        
        # todas las historias que son del autor y que ya son termiandas
        historias = obj.historias_set.all()
        # deserializamos ls historias
        deserialized = HistoriasBriefSerializer(historias, many=True)
        # retornamos la data
        return deserialized.data