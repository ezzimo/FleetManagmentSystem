from django.urls import path

from . import views

app_name = "delivery"

urlpatterns = [
    path("new_delivery", views.DeliveryCreateView.as_view(), name="delivery-creation"),
    path("delivery_details", views.DetailsDeliveryCreateView.as_view(), name="delivery-details"),
]
