from django.contrib import admin

from .models import Delivery, DeliveryDocuments, OperationDetails, Round, Subcontractor

admin.site.register(Delivery)
admin.site.register(DeliveryDocuments)
admin.site.register(OperationDetails)
admin.site.register(Round)
admin.site.register(Subcontractor)
