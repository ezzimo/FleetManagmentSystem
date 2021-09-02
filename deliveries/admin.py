from django.contrib import admin

from .models import Delivery, DeliveryDetails, Round, Subcontractor

admin.site.register(Delivery)
admin.site.register(DeliveryDetails)
admin.site.register(Round)
admin.site.register(Subcontractor)
