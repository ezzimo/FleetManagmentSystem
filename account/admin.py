from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.forms import RegistrationForm, UserChangeForm, UserCreationForm

from .models import Address, Bank, City, EmployeeSalary, Region, User


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
                    "website",
                    "ice",
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
                    "website",
                    "ice",
                    "mobile_2",
                    "landline",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )  # Other fields showed when creating an user


admin.site.register(Bank)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(EmployeeSalary)
admin.site.register(Address)
