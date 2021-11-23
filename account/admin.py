from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from account.forms import RegistrationForm, UserChangeForm, UserCreationForm

from .models import (
    Address,
    Bank,
    City,
    Client,
    Company,
    EmployeeSalary,
    FreeAddress,
    Region,
    User,
)


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "user_type",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "user_type",
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "email",
        "user_type",
    )
    ordering = (
        "email",
        "user_type",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_type",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "mobile",
                )
            },
        ),
        (
            "staff",
            {
                "fields": (
                    "registration_number",
                    "cni",
                    "picture",
                    "birth_date",
                    "birth_city",
                    "cnss_registration_number",
                    "recruitment_date",
                    "Contract_type",
                    "city_id",
                    "rib_bank",
                    "bank_address",
                    "bank_id",
                )
            },
        ),
        (
            "driver",
            {
                "fields": (
                    "driving_licence",
                    "driver_licence_expiration_date",
                    "glasses",
                    "glasses_certificat",
                )
            },
        ),
        (
            "customer",
            {
                "fields": (
                    "company_name",
                    "mobile_2",
                    "landline",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )  # Other fields showed when updating an user
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_type",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "mobile",
                )
            },
        ),
        (
            "staff",
            {
                "fields": (
                    "registration_number",
                    "cni",
                    "picture",
                    "birth_date",
                    "birth_city",
                    "cnss_registration_number",
                    "recruitment_date",
                    "Contract_type",
                    "city_id",
                    "rib_bank",
                    "bank_address",
                    "bank_id",
                )
            },
        ),
        (
            "driver",
            {
                "fields": (
                    "driving_licence",
                    "driver_licence_expiration_date",
                    "glasses",
                    "glasses_certificat",
                )
            },
        ),
        (
            "customer",
            {
                "fields": (
                    "company_name",
                    "mobile_2",
                    "landline",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )  # Other fields showed when creating an user


admin.site.register(Bank)
admin.site.register(Client)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(EmployeeSalary)
admin.site.register(FreeAddress)
admin.site.register(Company)


@admin.register(Address)
class AddressAdmin(OSMGeoAdmin):
    list_display = (
        "address_name",
        "customer",
        "phone",
        "postcode",
        "address_line_1",
        "address_line_2",
        "town_city",
        "town_region",
        "address_point",
        "delivery_instructions",
        "created_at",
        "updated",
        "default",
        "is_active",
    )
