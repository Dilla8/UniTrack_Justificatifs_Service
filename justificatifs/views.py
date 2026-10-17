from rest_framework import viewsets
from .models import Justificatif
from .serializer import JustificatifSerializer

class JustificatifViewSet(viewsets.ModelViewSet):
    queryset = Justificatif.objects.all()
    serializer_class = JustificatifSerializer