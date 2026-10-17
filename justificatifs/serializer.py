from rest_framework import serializers
from .models import Justificatif

class JustificatifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificatif
        fields = '__all__'