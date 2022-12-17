from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from .models import Address, User


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

    # Add form validation and error handling here
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise forms.ValidationError("Phone number is required")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Phone number must be between 10 and 15 digits long")
        return phone

    def clean_address_line_1(self):
        address_line_1 = self.cleaned_data.get("address_line_1")
        if not address_line_1:
            raise forms.ValidationError("Address line 1 is required")
        return address_line_1

    def clean_town_city(self):
        town_city = self.cleaned_data.get("town_city")
        if not town_city:
            raise forms.ValidationError("Town/City is required")
        return town_city

    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode")
        if not postcode:
            raise forms.ValidationError("Postcode is required")
        if len(postcode) < 6 or len(postcode) > 8:
            raise forms.ValidationError("Postcode must be between 6 and 8 characters long")
        return postcode


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

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise forms.ValidationError("Please enter a username")
        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long")
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not password:
            raise forms.ValidationError("Please enter a password")
        if len(password) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long")
        return password


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_("Enter First name"), min_length=4, max_length=50, help_text="Required", required=True)
    last_name = forms.CharField(label=_("Enter Last name"), min_length=4, max_length=50, help_text="Required", required=True)
    email = forms.EmailField(
        max_length=100, help_text=_("Required"), error_messages={"required": "Sorry, you will need an email"}, required=True
    )
    
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use. Please choose a different email.')
        return email


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("Enter First name"),
        min_length=4,
        max_length=50,
        help_text="Required",
        error_messages={
            "required": "First name is required",
            "min_length": "First name must be at least 4 characters",
            "max_length": "First name cannot be more than 50 characters",
        }
    )
    last_name = forms.CharField(
        label=_("Enter Last name"),
        min_length=4,
        max_length=50,
        help_text="Required",
        error_messages={
            "required": "Last name is required",
            "min_length": "Last name must be at least 4 characters",
            "max_length": "Last name cannot be more than 50 characters",
        }
    )
    email = forms.EmailField(
        max_length=100,
        help_text=_("Required"),
        error_messages={
            "required": "Email is required",
            "invalid": "Please enter a valid email address",
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        error_messages={
            "required": "Password is required",
        }
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput,
        error_messages={
            "required": "Confirm password is required",
        }
    )

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
        r = User.objects.filter(first_name=first_name, last_name=last_name)
        if r.count():
            raise forms.ValidationError("Name already exists")
        return first_name + " " + last_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match")
        return cd["password2"]



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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email
class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        help_text="Enter the email you used to register",
        error_messages={"invalid": "Please enter a valid email address"},
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user with this email.")
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

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

