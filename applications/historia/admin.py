from django.contrib import admin

# Models
from .models import Historias, Comentarios, Valoraciones

admin.site.register(Historias)
admin.site.register(Comentarios)
admin.site.register(Valoraciones)
