from django.urls import path

from . import views

app_name = "delivery"

urlpatterns = [
    path("", views.DeliveryCreateView.as_view(), name="delivery-creation"),
]
