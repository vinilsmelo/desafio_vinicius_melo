# waste_app/models.py
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver




class WasteStation(models.Model):
    name = models.CharField(max_length=255)
    volume_percentage = models.IntegerField(default=0)
    collection_requested = models.BooleanField(default=False)
    collection_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_history(self):
        return StationHistory.objects.filter(station=self)
    
@receiver(post_save, sender=WasteStation)
def create_station_history(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Criar entrada no histórico para a criação da estação
        operation = 'Create'
    else:
        # Criar entrada no histórico para alteração no volume
        operation = 'Volume Changed'

    StationHistory.objects.create(
        station=instance,
        operation=operation,
        old_volume_percentage=instance.volume_percentage,
        new_volume_percentage=instance.volume_percentage
    )


class StationHistory(models.Model):
    station = models.ForeignKey(WasteStation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    operation = models.CharField(max_length=20)
    old_volume_percentage = models.IntegerField()
    new_volume_percentage = models.IntegerField()

    def __str__(self):
        return f'{self.station.name} - {self.operation} - {self.timestamp}'

@receiver(post_migrate)
def create_default_stations(sender, **kwargs):
    if sender.name == 'waste_app':
        station1, _ = WasteStation.objects.get_or_create(name='Estação 1')
        station2, _ = WasteStation.objects.get_or_create(name='Estação 2')
        station3, _ = WasteStation.objects.get_or_create(name='Estação 3')

        # Adicione histórico para cada estação criada
        StationHistory.objects.create(station=station1, operation='Create', old_volume_percentage=0, new_volume_percentage=0)
        StationHistory.objects.create(station=station2, operation='Create', old_volume_percentage=0, new_volume_percentage=0)
        StationHistory.objects.create(station=station3, operation='Create', old_volume_percentage=0, new_volume_percentage=0)
