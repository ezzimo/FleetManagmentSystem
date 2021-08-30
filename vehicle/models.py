from datetime import date, datetime, timedelta

from django.conf import Settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Make(models.Model):
    """
    Table of different Make for Vehicles
    """

    name = models.CharField(max_length=125, unique=True)
    logo = models.ImageField(verbose_name=_("Logo"), help_text=_("Make Company logo"), upload_to="images/make/")
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Make")
        verbose_name_plural = _("Makes")

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    """
    Table of different Models existing for every Make
    """

    name = models.CharField(max_length=125, unique=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    gross_vehicle_weight = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name=_("Gross vehicle weight")
    )
    gross_combined_weight = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name=_("Gross combined weight")
    )
    total_length_L = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name=_("Total length L")
    )
    total_width_W = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name=_("Toltal width W")
    )

    class Meta:
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    """
    Table of detailled information about vehicles
    """

    serie = models.CharField(max_length=18, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=255)
    matricule = models.CharField(max_length=18, unique=True, blank=True, null=True)
    model = models.ForeignKey(VehicleModel, on_delete=CASCADE)
    picture = models.ImageField(
        verbose_name=_("Vehicle Picture"), help_text=_("Vehicle Picture "), upload_to="images/vehicle/"
    )
    ww = models.CharField(max_length=18, blank=True, null=True)
    entry_into_service = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    extinguisher = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, help_text=_("extincteur expiratiOn date")
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ["serie", "matricule"]
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def get_absolute_url(self):
        return reverse("vehicle:vehicle_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.serie)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.matricule


class VehicleSpecification(models.Model):
    """
    This table of Vehicle's models.
    """

    specification_name = models.CharField(
        verbose_name=_("Specification Name"), help_text=_("Required"), max_length=125
    )
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.RESTRICT)
    description = models.CharField(verbose_name=_("Description"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Modele Specification")
        verbose_name_plural = _("Modele Specifications")

    def __str__(self):
        return self.specification_name


class ModelSpecificationValue(models.Model):
    """
    Table of speciale caractere for the vahicle
    """

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    specification = models.ForeignKey(VehicleSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Vehicle specifications values (maximum of 255 carachteres)"),
        max_length=255,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Vehicle Specification Value")
        verbose_name_plural = _("Vehicle Specification Values")

    def __str__(self):
        return self.value


class AnssuranceCompany(models.Model):
    """
    Anssurance Company table
    """

    name = models.CharField(verbose_name=_("Name"), help_text=_("Anssurance Company Name"), max_length=255)
    logo = models.ImageField(
        verbose_name=_("Logo"), help_text=_("link to Anssurance Company logo"), upload_to="images/anssurance_company/"
    )
    email = models.EmailField(
        verbose_name=_("Email"), help_text=_("Anssurance Company Email"), max_length=65, unique=True
    )
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    seconde_phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(verbose_name=_("Address"), help_text=_("Anssurance Company Address"), max_length=255)
    city = models.CharField(verbose_name=_("City"), help_text=_("Anssurance Company City"), max_length=15)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Anssurance Company")
        verbose_name_plural = _("Anssurance Companies")

    def __str__(self):
        return self.name


class AnssuranceType(models.Model):
    """
    Different types of existing Anssurance.
    """

    company_name = models.ForeignKey(
        AnssuranceCompany, blank=True, null=True, verbose_name=_("company"), on_delete=models.CASCADE
    )
    anssurance_type = models.CharField(verbose_name=_("Assurance Type"), help_text=_("Required"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Anssurance Type")
        verbose_name_plural = _("Anssurance types")

    def __str__(self):
        return self.anssurance_type


class VehicleAnssuranceSpecification(models.Model):
    """
    Link betwen vehicles and different Anssurance types
    """

    vehicle = models.ForeignKey(Vehicle, blank=False, null=False, verbose_name=_("Vehicle"), on_delete=models.CASCADE)
    anssurance_type = models.ForeignKey(
        AnssuranceType, blank=False, null=False, verbose_name=_("Anssurance Type"), on_delete=models.CASCADE
    )
    effective_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    insurance_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    anssurance_document = models.ImageField(
        verbose_name=_("Document"), help_text=_("Copy of original Anssurance copy"), upload_to="images/anssurance/"
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Anssurance Specification")
        verbose_name_plural = _("Anssurance Specifications")

    def __str__(self):
        return self.anssurance_type.anssurance_type


class CertificatOfCerculation(models.Model):
    """
    Table of Circulation autorisation certificat
    """

    vehicle = models.ForeignKey(Vehicle, blank=True, null=True, on_delete=models.SET_NULL)
    effective_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cerculation_document = models.ImageField(
        verbose_name=_("Document"), help_text=_("Copy of original Anssurance copy"), upload_to="images/cerculation/"
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Cerculation Certificat")
        verbose_name_plural = _("Cerculation Certificats")

    def __str__(self):
        return self.vehicle


class CertificateOfFitness(models.Model):
    vehicle = models.ForeignKey("Vehicle", blank=True, null=True, on_delete=models.SET_NULL)
    effective_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cerculation_document = models.ImageField(
        verbose_name=_("Document"), help_text=_("Copy of original Fitness document"), upload_to="images/fitness/"
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Fitness Certificat")
        verbose_name_plural = _("Fitness Certificats")

    def __str__(self):
        return self.vehicle


class SpecialCertificat(models.Model):
    certificate_name = models.CharField(verbose_name=_("Special Certificat"), help_text=_("Required"), max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    effective_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cerculation_document = models.ImageField(
        verbose_name=_("Document"), help_text=_("Copy of original Fitness document"), upload_to="images/fitness/"
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Special Certificat")
        verbose_name_plural = _("Special Certificats")

    def __str__(self):
        return self.certificate_name
