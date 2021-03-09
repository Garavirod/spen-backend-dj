from django.db import models
from model_utils.models import TimeStampedModel
# Models
from applications.escritor.models import Usuarios

class Historias(TimeStampedModel):
    """ 
        Este calse define la estructura del modelo Historias,        
    """
    titulo = models.CharField(
        'titulo',
        max_length=200,
        blank=False
    )

    narrativa = models.CharField(
        'narrativa',
        max_length=20,
        blank=False        
    )

    genero = models.CharField(
        'genero',
        max_length=20,
        blank=True
    )

    sinopsis = models.TextField(
        'sinopsis',
        max_length=500,
        blank=True
    )

    contenido = models.TextField(
        'contenido',
        blank=True
    )

    status = models.BooleanField(
        'terminada', 
        default=False
    )

    # Un autor puede tener muchas historias
    autor = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        return self.titulo

class Comentarios(TimeStampedModel):
    """ 
        Este calse define la estructura del modelo cometario,        
    """
    contenido = models.TextField(
        'contenido',
        max_length=500
    )

    # Un autor puede hacer multiples comentarios
    autor_comentario = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE
    )

    # Una historia pude tener muchos comentarios y viceversa
    historia_comentario = models.ManyToManyField(Historias)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'comentarios'

    def __str__(self):
        return str(self.pk)

class Valoraciones(TimeStampedModel):
    """ 
        Esta clase define la estructura del modelo valoración  
    """
    puntaje = models.PositiveIntegerField('puntaje', default=0)

    # Un usuario pude hacer multiples valoraciuones
    autor_valoracion = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    # Una historai tiene muchas valoraciones
    historia_valoracion = models.ForeignKey(Historias, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'

    def __str__(self):
        return str(self.puntaje)