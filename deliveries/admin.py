from django.contrib import admin

from .models import Delivery, DeliveryItem

admin.site.register(Delivery)
admin.site.register(DeliveryItem)
