from django import forms
from django.forms import fields, widgets
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
        widgets = {
            "operation_date": forms.DateInput(
                format=("%d %B %Y"),
                attrs={"class": "form-control mb-2 delivery-form", "placeholder": "Select a date"},
            ),
            "document": forms.FileInput(attrs={"multiple": True}),
            "pickup_address": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name_reciever"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "full name reciever "}
        )
        self.fields["pickup_address"].widget.attrs.update(
            {"class": "form-control mb-2 dropdown delivery-form", "Placeholder": "pickup address "}
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
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
                "Placeholder": "delivery status",
            }
        )
        self.fields["delivery_key"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "delivery key"}
        )
        self.fields["billing_status"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "mb-2 form-check-input delivery-form",
                "Placeholder": "delivery status",
            }
        )
        self.fields["delivery_status"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "mb-2 form-check-input delivery-form",
                "Placeholder": "delivery status",
            }
        )


class DeliveryDetailsForm(forms.ModelForm):

    delivery = forms.CharField(
        label="delivery",
        widget=forms.Select(
            attrs={"class": "form-control mb-3", "placeholder": "delivery", "id": "form-delivery-details"}
        ),
    )
    round = forms.CharField(
        label="Round",
        widget=forms.Select(attrs={"class": "form-control mb-3", "placeholder": "Round", "id": "form-round"}),
    )
    is_subcontract = forms.BooleanField(
        label="Check if Subcontractor",
        widget=forms.RadioSelect(
            attrs={"class": "form-control mb-3", "placeholder": "Last name", "id": "form-is-subcontractor"}
        ),
    )
    subcontractor = forms.CharField(
        label="Subcontractor",
        widget=forms.Select(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-subcontractor"}
        ),
    )
    subcontract_price = forms.DecimalField(
        label="Subcontractor Price",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Price Subcontractor if any",
                "id": "form-Subcontractor-price",
            }
        ),
    )
    is_loader = forms.BooleanField(
        label="loader",
        widget=forms.RadioSelect(attrs={"class": "form-control mb-3", "placeholder": "Company ice", "id": "form-ice"}),
    )
    loader_price = forms.DecimalField(
        label="loader price",
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "Website", "id": "form-website"}),
    )
    is_commission = forms.BooleanField(
        label="commission",
        widget=forms.RadioSelect(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_2"}
        ),
    )
    commission_coast = forms.DecimalField(
        label="commission coast ",
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-3", "placeholder": "landline number", "id": "form-landline"}
        ),
    )
    is_driver_charges = forms.BooleanField(
        label="driver charges",
        widget=forms.RadioSelect(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_1"}
        ),
    )
    driver_charges_coast = forms.DecimalField(
        label="driver charges coast",
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-3", "placeholder": "Company name", "id": "form-company_name"}
        ),
    )
    distance = forms.IntegerField(
        label="distance",
        widget=forms.NumberInput(attrs={"class": "form-control mb-3", "placeholder": "Company ice", "id": "form-ice"}),
    )
    extra_time = forms.DurationField(
        label="extra time",
        widget=forms.TimeInput(attrs={"class": "form-control mb-3", "placeholder": "Website", "id": "form-website"}),
    )
    extra_time_coast = forms.DecimalField(
        label="extra time coast",
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-3", "placeholder": "mobile number", "id": "form-mobile_2"}
        ),
    )
    delivery_price = forms.DecimalField(
        label="delivery price",
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-3", "placeholder": "landline number", "id": "form-landline"}
        ),
    )

    class Meta:
        model = DeliveryDetails
        fields = (
            "delivery",
            "round",
            "is_subcontract",
            "subcontractor",
            "subcontract_price",
            "is_loader",
            "loader_price",
            "is_commission",
            "commission_coast",
            "is_driver_charges",
            "driver_charges_coast",
            "distance",
            "extra_time",
            "extra_time_coast",
            "delivery_price",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["delivery"].required = True
        self.fields["round"].required = True
        self.fields["delivery_price"].required = True
