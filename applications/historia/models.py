from django.db import models
from model_utils.models import TimeStampedModel
# Models
from applications.escritor.models import Usuarios

class Historias(TimeStampedModel):
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
        max_length=20
    )

    sinopsis = models.TextField(
        'sinopsis',
        max_length=500,
        default=''
    )

    contenido = models.TextField(
        'contenido',
        default=''
    )

    status = models.BooleanField('terminada', default=False)

    autor = models.ForeignKey(Usuarios,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        return self.titulo