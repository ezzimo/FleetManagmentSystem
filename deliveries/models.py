from account.models import Address, City, User
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from vehicle.models import Vehicle


class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("delivery_user"))
    full_name_reciever = models.CharField(_("Reciever Full Name"), max_length=50)
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name=_("pickup_address"))
    destination_address = models.CharField(max_length=250)
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name=_("delivery_city"))
    destination_post_code = models.CharField(max_length=20)
    operation_date = models.DateField(
        _("desired pickup date"), auto_now=False, auto_now_add=False, blank=False, null=False
    )
    boxes_number = models.PositiveIntegerField(_("Number of Boxes"), default=1)
    boxes_wight = models.PositiveIntegerField(_("Boxes Wight"), default=1)
    boxes_volume = models.PositiveIntegerField(_("Boxes Volume"), default=0)
    document = models.FileField(
        help_text=_("Delivery Documets"),
        verbose_name=_("Delivery Certificates"),
        upload_to="documents/deliveries_documents/",
    )
    invoice = models.BooleanField(_("check if you want an invoice"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    delivery_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")

    def __str__(self):
        return str(self.created_at)


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

    def __str__(self):
        return self.first_name + " " + self.last_name


class DeliveryDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("responsable_user"))
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name=_("delivery"))
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name=_("round"))
    is_subcontract = models.BooleanField(default=False)
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE, related_name=_("subcontractor"))
    subcontract_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_loader = models.BooleanField(default=False)
    loader_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_commission = models.BooleanField(default=False)
    commission_coast = models.DecimalField(max_digits=7, decimal_places=2)
    is_driver_charges = models.BooleanField(default=False)
    driver_charges_coast = models.DecimalField(max_digits=7, decimal_places=2)
    distance = models.PositiveSmallIntegerField(_("Approximative distance max=32767 km"), default=1)
    extra_time = models.DurationField(_("Extra time taken"))
    extra_time_coast = models.DecimalField(max_digits=7, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Delivery Details")
        verbose_name_plural = _("Deliveries Details")

    def __str__(self):
        return str(self.created_at)


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, related_name="deliveries", on_delete=models.CASCADE)
    product = models.ForeignKey(User, related_name="customer_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
