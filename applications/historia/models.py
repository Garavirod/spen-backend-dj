from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
# Models
from applications.escritor.models import Usuarios
# Managers
from .managers import StoriesManager

class Historias(TimeStampedModel):
    """ 
        Esta clase define la estructura del modelo Historias,        
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

    # Valoración de la historia
    puntaje = models.PositiveIntegerField('puntaje', default=0)

    # Un autor puede tener muchas historias
    autor = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE
    )

    # Manager

    objects = StoriesManager()

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        return str(self.pk) + ' - ' + self.titulo

class Comentarios(TimeStampedModel):
    """ 
        Esta clase define la estructura del modelo cometario,        
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
        return self.autor_comentario.email

class Valoraciones(TimeStampedModel):
    """ 
        Esta clase define la estructura del modelo valoración  
    """    
    # Puntaje asignado a la historia
    puntaje = models.PositiveIntegerField('puntaje', default=0)

    # Un usuario pude hacer multiples valoraciuones
    autor_valoracion = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    # Una historai tiene muchas valoraciones
    historia_valoracion = models.ForeignKey(Historias, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'
        # Un escritor no puede valorar una misma historia más de una véz
        # unique_together = ['autor_valoracion','historia_valoracion']

    def __str__(self):
        return str(self.historia_valoracion.titulo)


""" Signals """
@receiver(post_save, sender=Valoraciones)
def get_avg_valoracion(sender, instance, **kwargs):
    """ 
        Asigna el puntaje promedio a una historia 
        basado en el puntaje de la valoración que 
        se acaba de crear
    """
    if instance: # Recuperamos la instancia actual del modelo Sender
        # obtenemos el puntaje promedio de la historia valorada
        puntaje_calculado = Valoraciones.objects.filter(
            historia_valoracion=instance.historia_valoracion
        ).aggregate(Avg('puntaje', output_field=models.IntegerField()))
        # asiganamos el puntaje promedio a la instancia valorada
        instance.historia_valoracion.puntaje = puntaje_calculado['puntaje__avg']
        # guaradamos cambios en la instancia de la historia
        instance.historia_valoracion.save()        

@receiver(post_save, sender=Historias)
def increment_num_stoires(sender,instance, **kwargs):
    """ Actualiza el numero de historias publicadas 
        (status=true) del autor 
    """
    # Verificamos que la instancia tenga el atributo status en True
    if kwargs.get('status',True):
        # conseguimos todos las historiuas que han sido marcadas como termiandas
        num_historias = Historias.objects.filter(
            status=True,
            autor=instance.autor
        ).count()
        # asignamos la cantida de historias que han sido publicadas
        instance.autor.libros_publicados = num_historias
        # guardamos cambios en BDD
        instance.autor.save()