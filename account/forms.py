from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.gis import forms as gis_form
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.enums import Choices
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from .models import Address, Client, User

# from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget


class UserAddressForm(forms.ModelForm):
    customer = forms.Select(attrs={"help_text": "obligatoire"})
    address_point = gis_form.PointField(
        widget=gis_form.OSMWidget(
            attrs={
                "map_width": 300,
                "map_height": 200,
                "default_lat": 33.575729,
                "default_lon": -7.706956,
                "default_zoom": 9,
            }
        )
    )

    class Meta:
        model = Address
        fields = [
            "address_name",
            "customer",
            "phone",
            "address_line_1",
            "address_line_2",
            "town_city",
            "town_region",
            "postcode",
            "address_point",
            "delivery_instructions",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "address name"}
        )
        self.fields["customer"].widget.attrs.update({"class": "form-control mb-2 account-form"})
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "Placeholder": "phone"})
        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "address "}
        )
        self.fields["address_line_2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "address"}
        )
        self.fields["town_city"].widget.attrs.update({"class": "form-control mb-2 account-form"})
        self.fields["town_region"].widget.attrs.update({"class": "form-control mb-2 account-form"})
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "postcode"}
        )
        self.fields["delivery_instructions"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "delivery instructions"}
        )


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Username", "id": "login-username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_("Enter First name"), min_length=4, max_length=50, help_text="Required")
    last_name = forms.CharField(label=_("Enter Last name"), min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        max_length=100, help_text=_("Required"), error_messages={"Required": "Sorry, you will need an email"}
    )
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def clean_username(self):
        first_name = self.cleaned_data["first_name"].lower()
        last_name = self.cleaned_data["last_name"].lower()
        if User.objects.filter(first_name__exact=first_name, last_name__exact=last_name).exists():
            raise forms.ValidationError("Ce Nom et Prenom existent")
        return first_name + " " + last_name

    def clean_password2(self):
        # cd = self.cleaned_data
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passes sont differents")

        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Prenom"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Nom"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Repeat Password"})


class ClientRegistrationForm(forms.ModelForm):
    class TypeOfContract(models.TextChoices):
        PERMANENT = "Per.", _("Permanent")
        TEMPORAIRE = "Tem.", _("Temporaire")

    first_name = forms.CharField(label=_("Prenom"), min_length=4, max_length=50, help_text="obligatoire")
    last_name = forms.CharField(label=_("Nom"), min_length=4, max_length=50, help_text="obligatoire")
    email = forms.EmailField(min_length=4, max_length=100, label=_("Email"), help_text="exemple@site.com")
    company_name = forms.CharField(label=_("Nom de Société"), min_length=4, max_length=50, help_text="obligatoire")
    ice = forms.CharField(label=_("ICE"), min_length=4, max_length=50, help_text="obligatoire")
    website = forms.CharField(label="site-web", min_length=10)
    mobile = forms.CharField(label="Portable", widget=forms.NumberInput, help_text="0123456789")
    mobile_2 = forms.CharField(label="Portable 2", widget=forms.NumberInput, help_text="0123456789")
    landline = forms.CharField(
        label="Telephone fixe", widget=forms.NumberInput, min_length=10, max_length=13, help_text="0123456789"
    )
    Contract_type = forms.ChoiceField(choices=TypeOfContract.choices, label="Type de Contrat", widget=forms.Select)

    class Meta:
        model = Client
        fields = (
            "first_name",
            "last_name",
            "company_name",
            "email",
            "ice",
            "website",
            "mobile",
            "mobile_2",
            "landline",
            "Contract_type",
        )

    def clean_username(self):
        first_name = self.cleaned_data["first_name"].lower()
        last_name = self.cleaned_data["last_name"].lower()
        if User.objects.filter(first_name__exact=first_name, last_name__exact=last_name).exists():
            raise forms.ValidationError("Ce Nom et Prenom existent")
        return first_name + " " + last_name

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("s'il vous plait choisissez une autre addresse, celle ci existe deja")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "First name"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Last name"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["company_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Nom Société"})
        self.fields["ice"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "ICE"})
        self.fields["mobile"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "0123456789"})
        self.fields["mobile_2"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "0123456789"})
        self.fields["landline"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "0123456789"})
        self.fields["website"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "site-web Société"})
        self.fields["Contract_type"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Type Contract"}
        )


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Email",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )
    first_name = forms.CharField(
        label="Prénom",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "first name", "id": "form-firstname"}
        ),
    )
    last_name = forms.CharField(
        label="Nom",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Last name", "id": "form-lastname"}
        ),
    )
    mobile = forms.CharField(
        label="Mobile 1",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_1"}
        ),
    )
    company_name = forms.Select(
        label="Compagnie",
        min_length=4,
        max_length=50,
        attrs={"class": "form-control mb-3", "placeholder": "Nom de la Compagnie", "id": "form-company_name"},
    )
    ice = forms.CharField(
        label="ICE",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Compagnie ice", "id": "form-ice"}),
    )
    website = forms.CharField(
        label="Site",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Website", "id": "form-website"}),
    )
    mobile_2 = forms.CharField(
        label="Mobile 2",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_2"}
        ),
    )
    landline = forms.CharField(
        label="Tel. Fixe",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "landline number", "id": "form-landline"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "mobile",
            "company_name",
            "website",
            "ice",
            "mobile_2",
            "landline",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["mobile"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        usr = User.objects.filter(email=email)
        if not usr:
            raise forms.ValidationError("Unfortunatley we can not find that email address")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-newpass"}
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-new-pass2"}
        ),
    )
