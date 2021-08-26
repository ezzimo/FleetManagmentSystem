from django.urls import path

from . import views

app_name = "vehicle"

urlpatterns = [
    path("", views.vehicle_all, name="vehicles_all"),
    path("VehicleCreation", views.VehicleCreationView.as_view(), name="vehicle-creation"),
    path("<slug:slug>", views.vehicle_detail, name="vehicle_detail"),
    path("<int:pk>/VehicleUpdate", views.VehicleUpdateView.as_view(), name="vehicle-update"),
    path("<int:pk>VehicleDeletion", views.VehicleDeleteView.as_view(), name="vehicle-delete"),
]
