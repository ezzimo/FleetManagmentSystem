import datetime
import json

import requests
from account.models import Address, Bank, City, Client, User
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from humanfriendly import format_timespan
from vehicle.models import Vehicle


class Delivery(models.Model):
    user = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("Client"), related_name=_("delivery_user")
    )
    user_pickup = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("donneur"), related_name=_("user_pickup"), default=False
    )
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name=_("pickup_address"))
    user_reciever = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_("receveur"),
        related_name=_("user_reciever"),
        default=False,
    )
    destination_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name=_("destination_address"))
    operation_date = models.DateField(
        _("desired pickup date"), auto_now=False, auto_now_add=False, blank=False, null=False
    )
    operation_time = models.TimeField(
        _("desired pickup date"), auto_now=False, auto_now_add=False, blank=False, null=False
    )
    google_distance_value = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    geo_distance_value = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    google_duration_value = models.DurationField(blank=True, null=True)
    boxes_number = models.PositiveIntegerField(_("Nombre des Boites"), default=1)
    boxes_wight = models.PositiveIntegerField(_("Poids de Boites"), default=1)
    boxes_volume = models.PositiveIntegerField(_("Volume des Boites"), default=0)
    invoice = models.BooleanField(_("check if you want an invoice"), default=False)
    confirmed = models.BooleanField(_("confirmed Delivery"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    delivery_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")

    def get_absolute_url(self):
        return reverse("delivery:unconf-delivery-details", args=[self.id])

    def save(self, *args, **kwargs):
        distance = self.distance
        self.google_distance_value = distance["google_distance"]
        self.geo_distance_value = distance["distance"]
        self.google_duration_value = distance["google_duration"]
        super().save(*args, **kwargs)

    @property
    def distance(self):
        distance = Distance(
            m=self.pickup_address.address_point.transform(32148, clone=True).distance(
                self.destination_address.address_point.transform(32148, clone=True)
            )
        )
        origin_lat = self.pickup_address.address_point.coords[1]
        origin_lon = self.pickup_address.address_point.coords[0]
        destination_lat = self.destination_address.address_point.coords[1]
        destination_lon = self.destination_address.address_point.coords[0]
        origin = f"{origin_lat},{origin_lon}"
        destination = f"{destination_lat},{destination_lon}"
        gl_json_distance = requests.get(
            "https://maps.googleapis.com/maps/api/directions/json?",
            params={
                "origin": origin,
                "destination": destination,
                "key": settings.GOOGLE_API_KEY,
            },
        )
        gl_distance = gl_json_distance.json()
        distance_gl = 0
        duration_gl = 0
        context = {}
        if gl_distance["status"] == "OK":
            routes = gl_distance["routes"][0]["legs"]
            for route in range(len(routes)):
                distance_gl += int(routes[route]["distance"]["value"])
                duration_gl += int(routes[route]["duration"]["value"])
        context["google_distance"] = f"{round(distance_gl / 1000, 2)}"
        context["google_duration"] = datetime.timedelta(seconds=duration_gl)
        context["distance"] = f"{round(distance.m / 1000, 2)}"
        print(context)

        return context

    def __str__(self):
        return str(self.delivery_key)


class DeliveryDocuments(models.Model):
    delivery = models.ForeignKey(
        Delivery, on_delete=models.SET_NULL, related_name=_("delivery_documents"), blank=True, null=True
    )
    document = models.FileField(
        help_text=_("Delivery Documets"),
        verbose_name=_("Delivery Certificates"),
        upload_to="documents/deliveries_documents/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at", "delivery")
        verbose_name = _("Delivery Documents")
        verbose_name_plural = _("Deliveries Documents")

    def __str__(self):
        return str(self.delivery)


class Round(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name=_("vehicle"))
    round_date = models.DateTimeField(_("Round Date"), auto_now_add=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")

    def __str__(self):
        return str(self.created_at)


class Subcontractor(models.Model):
    first_name = models.CharField(_("First Name"), max_length=150, unique=True)
    last_name = models.CharField(_("Last Name"), max_length=150, unique=True)
    is_company = models.BooleanField(_("Is Active"), default=False)
    company_name = models.CharField(_("Company Name"), max_length=150, unique=True)
    ice = models.PositiveIntegerField(_("ICE of the Company"), unique=True, null=True, blank=True)
    email = models.EmailField(_("Email Address"), unique=True)
    mobile = models.CharField(_("Mobile Number"), max_length=150, blank=True)
    mobile_2 = models.CharField(_("Mobile Number"), max_length=150, blank=True)
    landline = models.CharField(_("Landline Number"), max_length=150, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name=_("contractor_city"))
    address_line_1 = models.CharField(_("Address Line 1"), max_length=255)
    address_line_2 = models.CharField(_("Address Line 2"), max_length=255)
    is_active = models.BooleanField(_("Is Active"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name=_("subcontractor_vehicle"))

    class Meta:
        verbose_name = "Subcontractor"
        verbose_name_plural = "Subcontractor"

    def get_absolute_url(self):
        return reverse("delivery:subcontractor-details", args=[self.id])

    def __str__(self):
        return self.first_name + " " + self.last_name


class OperationDetails(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name=_("delivery"))
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name=_("round"), blank=True, null=True)
    is_subcontract = models.BooleanField(default=False, blank=True, null=True)
    subcontractor = models.ForeignKey(
        Subcontractor, on_delete=models.CASCADE, related_name=_("subcontractor"), blank=True, null=True
    )
    subcontract_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_loader = models.BooleanField(default=False, blank=True, null=True)
    loader_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_commission = models.BooleanField(default=False, blank=True, null=True)
    commission_coast = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_driver_charges = models.BooleanField(default=False, blank=True, null=True)
    driver_charges_coast = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    distance = models.DecimalField(_("Distance Approximative "), max_digits=7, decimal_places=2)
    extra_time = models.DurationField(_("Extra time taken"), blank=True, null=True)
    extra_time_coast = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    delivery_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Delivery Details")
        verbose_name_plural = _("Deliveries Details")

    def get_absolute_url(self):
        return reverse("delivery:operation-detail", args=[self.id])

    def __str__(self):
        return str(self.created_at)


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, related_name="deliveries", on_delete=models.CASCADE)
    product = models.ForeignKey(User, related_name="customer_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
