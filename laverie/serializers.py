from rest_framework import serializers
from models import *


class AppareilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appareil
        fields = '__all__'


class UtilisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utilisation
        fields = '__all__'
        