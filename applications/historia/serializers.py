# Third partty apps
from rest_framework import serializers
# Models
from .models import Historias
class NewStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Historias
        fields = ['titulo','narrativa','genero']