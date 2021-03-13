# dajngo
from django.contrib.auth.models import BaseUserManager
from django.db import models

class StoriesManager(models.Manager):
    def stories_fillter(self,titulo,narrativa,owner=None,writter=None):
        historias = None
        if owner:
            historias = self.filter(autor__id=owner)
        elif writter:
            historias = self.filter(autor__id=writter, status=True)
        else:
            historias = self.filter(status=True)

        if not narrativa and titulo:           
            # Filtrar por titulo    
            return historias.filter(titulo__icontains=titulo).order_by('created')        
        if not titulo and narrativa:
            # Filtrar por narrativa        
            return historias.filter(narrativa=narrativa).order_by('created')     
        else:           
            # filtrar por narrativa y titulo
            return historias.filter(                           
                titulo__icontains=titulo,
                narrativa__icontains=narrativa
            ).order_by('created')
