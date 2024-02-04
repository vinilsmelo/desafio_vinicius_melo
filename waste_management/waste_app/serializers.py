# waste_app/serializers.py
from rest_framework import serializers
from .models import WasteStation, StationHistory

class WasteStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteStation
        fields = ('id', 'name', 'volume_percentage', 'collection_requested', 'collection_confirmed')

class StationHistorySerializer(serializers.ModelSerializer):
    station = WasteStationSerializer()  # Use o WasteStationSerializer como um campo aninhado

    class Meta:
        model = StationHistory
        fields = ('id', 'station', 'timestamp', 'operation', 'old_volume_percentage', 'new_volume_percentage')

