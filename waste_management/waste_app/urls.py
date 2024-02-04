# waste_app/urls.py

from django.urls import path
from .views import WasteStationListCreateView, WasteStationRetrieveUpdateDeleteView
from .views import WasteStationListCreateView, WasteStationRetrieveUpdateDeleteView, StationHistoryListView

urlpatterns = [
    path('waste_stations/', WasteStationListCreateView.as_view(), name='waste-stations-list-create'),
    path('waste_stations/<int:pk>/', WasteStationRetrieveUpdateDeleteView.as_view(), name='waste-stations-retrieve-update-delete'),
    path('waste_stations/', WasteStationListCreateView.as_view(), name='waste_station_list_create'),
    path('waste_stations/<int:pk>/', WasteStationRetrieveUpdateDeleteView.as_view(), name='waste_station_retrieve_update_delete'),
    path('waste_stations/<int:station_id>/history/', StationHistoryListView.as_view(), name='station_history_list'),
]
