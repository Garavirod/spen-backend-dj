# Third partty apps
from rest_framework import serializers
# Models
from .models import Historias
from applications.escritor.models import Usuarios


class NewStorySerializer(serializers.ModelSerializer):
    """ Serializador para crear una nueva historia """
    class Meta:
        model = Historias
        fields = ['titulo','narrativa','genero']

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

class  HistoriasBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historias
        exclude = ['autor','contenido']

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

class MyProfileSerializer():
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