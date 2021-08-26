from django import forms
from django.contrib import admin

from .models import (
    AnssuranceCompany,
    AnssuranceType,
    CertificateOfFitness,
    CertificatOfCerculation,
    Make,
    ModelSpecificationValue,
    SpecialCertificat,
    Vehicle,
    VehicleAnssuranceSpecification,
    VehicleModel,
    VehicleSpecification,
)

admin.site.register(Make)
admin.site.register(AnssuranceType)
admin.site.register(AnssuranceCompany)


class VehicleSpecificationInline(admin.TabularInline):
    model = VehicleSpecification


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    inlines = [
        VehicleSpecificationInline,
    ]


class ModelSpecificationValueInline(admin.TabularInline):
    model = ModelSpecificationValue


class VehicleAnssuranceSpecificationInline(admin.TabularInline):
    model = VehicleAnssuranceSpecification


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [
        ModelSpecificationValueInline,
        VehicleAnssuranceSpecificationInline,
    ]
