from rest_framework import serializers
from .models import Cow, Scan
class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'
class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'