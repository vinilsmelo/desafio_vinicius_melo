# waste_app/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import WasteStation, StationHistory
from .serializers import WasteStationSerializer, StationHistorySerializer

class StationHistoryListView(generics.ListAPIView):
    serializer_class = StationHistorySerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        return StationHistory.objects.filter(station_id=station_id)

class WasteStationListCreateView(generics.ListCreateAPIView):
    queryset = WasteStation.objects.all()
    serializer_class = WasteStationSerializer

    def create_history_entry(self, station, operation, old_volume, new_volume):
        StationHistory.objects.create(
            station=station,
            operation=operation,
            old_volume_percentage=old_volume,
            new_volume_percentage=new_volume
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        station = serializer.instance
        old_volume = station.volume_percentage

        if old_volume >= 80:
            station.collection_requested = True
            station.save()
            self.create_history_entry(station, 'CollectRequest', old_volume, old_volume)

        self.create_history_entry(station, 'VolumeChange', old_volume, station.volume_percentage)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WasteStationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WasteStation.objects.all()
    serializer_class = WasteStationSerializer

    def create_history_entry(self, station, operation, old_volume, new_volume):
        StationHistory.objects.create(
            station=station,
            operation=operation,
            old_volume_percentage=old_volume,
            new_volume_percentage=new_volume
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        old_volume = instance.volume_percentage

        if old_volume >= 80:
            instance.collection_confirmed = True
            instance.volume_percentage = 0
            instance.save()
            self.create_history_entry(instance, 'CollectConfirmation', old_volume, 0)

        return self.destroy(request, *args, **kwargs)

