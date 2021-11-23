import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.gis.db import models as gis_models
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    bank_name = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"


class Region(models.Model):
    region = models.CharField(max_length=128)

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class City(models.Model):
    city = models.CharField(max_length=128)
    region_id = models.ForeignKey("Region", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class FreeAddress(models.Model):
    """
    Adresses libres
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_name = models.CharField(_("Nom d'Adresse"), max_length=50)
    postcode = models.CharField(_("Code-Postale"), max_length=50)
    address_line_1 = models.CharField(_("Adresse Ligne 1"), max_length=255)
    address_line_2 = models.CharField(_("Adresse Ligne 2"), max_length=255)
    town_city = models.ForeignKey(City, verbose_name=_("Ville"), null=True, on_delete=models.SET_NULL)
    town_region = models.ForeignKey(Region, verbose_name=_("Region"), null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)

    class Meta:
        verbose_name = "Free Address"
        verbose_name_plural = "Free Addresses"

    def __str__(self):
        return self.address_name


class Company(models.Model):
    name = models.CharField(_("Nom de la Société"), max_length=256, unique=True, blank=False, null=False)
    address = models.ForeignKey(
        FreeAddress, null=True, blank=True, related_name="company_adresse", on_delete=models.SET_NULL
    )
    phone = models.CharField(_("Mobile Number"), max_length=150, blank=True)
    website = models.CharField(_("Site Web"), max_length=150, blank=True)
    natonale_transp_autorization = models.CharField(
        _("Autorisation de Transport National N°"), max_length=30, blank=True, null=True
    )
    internatonale_transp_commissionnaire = models.CharField(
        _("Commissionnaire de Transport International N°"), max_length=30, blank=True, null=True
    )
    comerce_registre = models.IntegerField(_("Registre de Comerce N°"), blank=True, null=True, default=1)
    cnss_matricule = models.IntegerField(_("CNSS matricule N°"), blank=True, null=True, default=1)
    patente = models.IntegerField(_("Patente N°"), blank=True, null=True, default=1)
    identifiant_fiscale = models.IntegerField(_("Identifiant Fiscal N°"), blank=True, null=True, default=1)
    ice = models.CharField(_("ICE N°"), blank=True, null=True, max_length=50)
    bank = models.ForeignKey(Bank, null=True, blank=True, on_delete=models.SET_NULL)
    bank_address = models.ForeignKey(
        FreeAddress, null=True, blank=True, related_name="Banque_adresse", on_delete=models.SET_NULL
    )
    rib = models.CharField(_("RIB"), max_length=120, blank=True, null=True)
    logo = models.ImageField(
        verbose_name=_("Logo"), help_text=_("Company logo"), upload_to="images/company/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def get_absolute_url(self):
        return reverse("account:company-detail", args=[self.id])

    def __str__(self):
        return self.name


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Supperuser must be assigned to is_staff."))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be assigned to is_superuser."))

        return self.create_user(email, first_name, last_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class TypeOfContract(models.TextChoices):
        PERMANENT = "Per.", _("Permanent")
        TEMPORAIRE = "Tem.", _("Temporaire")

    class UserTypes(models.TextChoices):
        OPERATOR = "op", _("Operator")
        ADMINISTRATION = "ad", _("Administration")
        Driver = "dr", _("Driver")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    user_type = models.CharField(max_length=2, choices=UserTypes.choices, default="op")
    email = models.EmailField(_("Email Address"), unique=True)
    first_name = models.CharField(_("First Name"), max_length=150, unique=True)
    last_name = models.CharField(_("Last Name"), max_length=150, unique=True)
    mobile = models.CharField(_("Mobile Number"), max_length=150, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=False)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    registration_number = models.PositiveSmallIntegerField(_("Driver Registration Number"), null=True, blank=True)
    cni = models.CharField(_("National Identity Code"), max_length=8, null=True, blank=True)
    picture = models.ImageField(
        verbose_name=_("Driver Pic"),
        help_text=_("Driver Identity Picture"),
        upload_to="images/driver/",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(_("Date Birth of the Driver"), null=True, blank=True)
    birth_city = models.CharField(_("Birth City of the Driver"), max_length=150, null=True, blank=True)
    cnss_registration_number = models.PositiveIntegerField(_("CNSS Registration Number"), null=True, blank=True)
    recruitment_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    Contract_type = models.CharField(
        max_length=4, choices=TypeOfContract.choices, default=TypeOfContract.PERMANENT, blank=True
    )
    city_id = models.ForeignKey("City", blank=True, null=True, on_delete=models.SET_NULL)
    rib_bank = models.PositiveIntegerField(_("RIB of the Driver Bank"), null=True, blank=True)
    bank_address = models.CharField(blank=True, null=True, max_length=100)
    bank_id = models.ForeignKey("Bank", blank=True, null=True, on_delete=models.SET_NULL)
    driving_licence = models.ImageField(
        verbose_name=_("Driver Licence"),
        help_text=_("Driver Licence Picture"),
        upload_to="images/driver_licence/",
        blank=True,
        null=True,
    )
    driver_licence_expiration_date = models.DateField(_("Expiration Date for Driver Licence"), null=True, blank=True)
    glasses = models.BooleanField(_("if the Driver use Glasses"), default=False)
    glasses_certificat = models.ImageField(
        verbose_name=_("Driver Glasse Certificate"),
        help_text=_("Driver Glasses Certificat Picture"),
        upload_to="images/driver_glasse_certificate/",
        null=True,
        blank=True,
    )
    company_name = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    mobile_2 = models.CharField(_("Mobile Number"), max_length=150, null=True, blank=True)
    landline = models.CharField(_("Landline Number"), max_length=150, null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "l@1.com",
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.first_name


class Client(models.Model):
    class TypeOfContract(models.TextChoices):
        PERMANENT = "Per.", _("Permanent")
        TEMPORAIRE = "Tem.", _("Temporaire")

    email = models.EmailField(_("Email Address"), null=True, blank=True, unique=True)
    first_name = models.CharField(_("First Name"), null=True, blank=True, max_length=150, unique=True)
    last_name = models.CharField(_("Last Name"), null=True, blank=True, max_length=150, unique=True)
    company_name = models.CharField(_("Company Name"), max_length=150, null=True, blank=True)
    ice = models.PositiveIntegerField(_("ICE of the Company"), unique=True, null=True, blank=True)
    mobile = models.CharField(_("Mobile Number"), max_length=150, blank=True)
    mobile_2 = models.CharField(_("Mobile Number"), max_length=150, null=True, blank=True)
    landline = models.CharField(_("Landline Number"), max_length=150, null=True, blank=True)
    Contract_type = models.CharField(
        max_length=4, choices=TypeOfContract.choices, default=TypeOfContract.PERMANENT, blank=True
    )
    website = models.CharField(_("Company website"), max_length=150, null=True, unique=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Client Account"
        verbose_name_plural = "Clients Accounts"

    def get_absolute_url(self):
        return reverse("account:client-detail", args=[self.id])

    def __str__(self):
        return self.first_name + " " + self.last_name


class EmployeeSalary(models.Model):
    class PaymentMode(models.TextChoices):
        VIREMENT = "Vir", _("Virement")
        ESPECES = "Esp", _("Especes")

    employee = models.ForeignKey("User", blank=False, null=False, on_delete=models.CASCADE)
    salary = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name=_("Employee Salary")
    )
    payment_mode = models.CharField(max_length=3, choices=PaymentMode.choices, default=PaymentMode.VIREMENT)
    is_active = models.BooleanField(_("Is Active"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Salary")
        verbose_name_plural = _("Salaris")

    def __str__(self):
        return self.employee


class Address(models.Model):
    """
    Adresses Clients
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_name = models.CharField(_("Nom d'Adresse"), max_length=50)
    customer = models.ForeignKey(Client, verbose_name=_("Client"), on_delete=models.CASCADE)
    phone = models.CharField(_("Phone N°"), max_length=50)
    postcode = models.CharField(_("Code-Postale"), max_length=50)
    address_line_1 = models.CharField(_("Adresse Ligne 1"), max_length=255)
    address_line_2 = models.CharField(_("Adresse Ligne 2"), max_length=255)
    town_city = models.ForeignKey(City, verbose_name=_("Ville"), null=True, on_delete=models.SET_NULL)
    town_region = models.ForeignKey(Region, verbose_name=_("Region"), null=True, on_delete=models.SET_NULL)
    address_point = gis_models.PointField(blank=True, null=True)
    delivery_instructions = models.CharField(
        _("Instructions de Livraison"), max_length=255, default="Pas d'instructions", null=True, blank=True
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address_name
