# waste_app/admin.py

from django.contrib import admin
from .models import WasteStation
from .models import WasteStation, StationHistory

#admin.site.register(WasteStation)

@admin.register(WasteStation)
class WasteStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'volume_percentage', 'collection_requested', 'collection_confirmed')

@admin.register(StationHistory)
class StationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'timestamp', 'operation',  'new_volume_percentage')