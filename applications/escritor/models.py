from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Managers
from .managers import UserManager
# Create your models here.


def custom_upload_image_to(instance,filename):
    try:
        old_instance = Usuarios.objects.get(pk=instance.pk)
        old_instance.imageProfile.delete()
        return 'profileImage/' + filename
    except:
        return 'profileImage/' + filename

class Usuarios(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    username = models.CharField(
        'Username',
        max_length=20,        
        blank=False  
    )

    email = models.EmailField(unique=True)

    aboutme = models.TextField(default='Nothing yet')

    gender = models.CharField(        
        max_length = 1,
        choices = GENDER_CHOICES,
        blank=False
    )
    
    imageProfile = models.ImageField(
        'profileImage',        
        upload_to=custom_upload_image_to        
    )

    # Crear un usuaario a partir del campo  email
    USERNAME_FIELD = 'email'

    # redefinicion de los atributos is_staf e is_active por defecto del AbstractUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # conectar el manager para la creación de ususario
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return str(self.pk) + " " + self.email