from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "phone",
            "address_line_1",
            "address_line_2",
            "town_city",
            "postcode",
            "delivery_instructions",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "Placeholder": "phone"})
        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "address "}
        )
        self.fields["address_line_2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "address"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "Placeholder": "town city"}
        )
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


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Enter First name"), min_length=4, max_length=50, help_text="Required")
    last_name = forms.CharField(label=_("Enter Last name"), min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        max_length=100, help_text=_("Required"), error_messages={"Required": "Sorry, you will need an email"}
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def clean_username(self):
        first_name = self.cleaned_data["first_name"].lower()
        last_name = self.cleaned_data["last_name"].lower()
        r = Customer.objects.filter(first_name=first_name, last_name=last_name)
        if r.count():
            raise forms.ValidationError("Name already exists")
        return first_name + " " + last_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "First name"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Last name"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat Password"})


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )
    first_name = forms.CharField(
        label="User name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "first name", "id": "form-firstname"}
        ),
    )
    last_name = forms.CharField(
        label="User name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Last name", "id": "form-lastname"}
        ),
    )
    mobile = forms.CharField(
        label="User mobile 1",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_1"}
        ),
    )
    company_name = forms.CharField(
        label="Company name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Company name", "id": "form-company_name"}
        ),
    )
    ice = forms.CharField(
        label="Company ice",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Company ice", "id": "form-ice"}),
    )
    website = forms.CharField(
        label="website",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Website", "id": "form-website"}),
    )
    mobile_2 = forms.CharField(
        label="User mobile 2",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_2"}
        ),
    )
    landline = forms.CharField(
        label="User landline",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "landline number", "id": "form-landline"}
        ),
    )

    class Meta:
        model = Customer
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
        usr = Customer.objects.filter(email=email)
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
