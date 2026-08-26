from django.shortcuts import render
from rest_framework import viewsets
from .models import Cow, Scan
from .serializers import CowSerializer, ScanSerializer
class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer


class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
