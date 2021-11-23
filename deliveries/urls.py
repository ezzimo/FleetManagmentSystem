from django.urls import path

from .views import *

app_name = "delivery"

urlpatterns = [
    path("deliveries", DeliveryListView.as_view(), name="deliveries"),
    path("new_delivery", DeliveryCreateView.as_view(), name="delivery-creation"),
    path("<pk>/unconfirmed_delivery", DeliveryDetailView.as_view(), name="unconf-delivery-details"),
    path("<pk>/update_delivery", DeliveryUpdateView.as_view(), name="update-delivery"),
    path("<pk>/delete_delivery", DeliveryDeleteeView.as_view(), name="delete-delivery"),
    path("operation/<pk>/operation_details", OperationCreateView.as_view(), name="operation-form"),
    path("<int:pk>/", OperationDetailView.as_view(), name="operation-detail"),
]
