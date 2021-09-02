from django import forms
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from .models import Delivery, DeliveryDetails, Round, Subcontractor


class UserDeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "full_name_reciever",
            "pickup_address",
            "destination_address",
            "destination_city",
            "destination_post_code",
            "operation_date",
            "boxes_number",
            "boxes_wight",
            "boxes_volume",
            "document",
            "invoice",
            "delivery_key",
            "billing_status",
            "delivery_status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name_reciever"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "full name reciever"}
        )
        self.fields["pickup_address"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "pickup address "}
        )
        self.fields["destination_address"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "destination address"}
        )
        self.fields["destination_city"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "destination city"}
        )
        self.fields["destination_post_code"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Post Code"}
        )
        self.fields["operation_date"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "operation date"}
        )
        self.fields["boxes_number"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "boxes number"}
        )
        self.fields["boxes_wight"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "boxes wight"}
        )
        self.fields["boxes_volume"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "boxes volume"}
        )
        self.fields["document"].widget.attrs.update(
            {"multiple": True, "class": "form-control mb-2 delivery-form", "Placeholder": "document"}
        )
        self.fields["invoice"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "invoice"}
        )
        self.fields["delivery_key"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "delivery key"}
        )
        self.fields["billing_status"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "billing status"}
        )
        self.fields["delivery_status"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "delivery status"}
        )


"""
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
"""
