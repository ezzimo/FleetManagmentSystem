from django import forms
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _

from .models import Delivery, DeliveryDocuments, OperationDetails, Round, Subcontractor


class UserDeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "user",
            "user_pickup",
            "pickup_address",
            "user_reciever",
            "destination_address",
            "operation_date",
            "operation_time",
            "boxes_number",
            "boxes_wight",
            "boxes_volume",
            "invoice",
            "delivery_key",
            "billing_status",
            "delivery_status",
        ]
        widgets = {
            "operation_date": forms.DateInput(
                format=("%d %B %Y"),
                attrs={"class": "form-control mb-2 delivery-form", "placeholder": "JJ-MM-AAAA"},
            ),
            "operation_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control mb-2 delivery-form"},
            ),
            "user": forms.Select(),
            "user_pickup": forms.Select(),
            "pickup_address": forms.Select(),
            "user_reciever": forms.Select(),
            "destination_address": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].widget.attrs.update({"class": "form-control mb-2 delivery-form", "Placeholder": "Client "})
        self.fields["user_pickup"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Emeteur "}
        )
        self.fields["pickup_address"].widget.attrs.update(
            {"class": "form-control mb-2 dropdown delivery-form", "Placeholder": "Addresse de ramassage "}
        )
        self.fields["user_reciever"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Receveur "}
        )
        self.fields["destination_address"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Addresse de destination"}
        )
        self.fields["boxes_number"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Nombre de Boites"}
        )
        self.fields["boxes_wight"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Poids de la marchandise"}
        )
        self.fields["boxes_volume"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Volume de la marchandise"}
        )
        self.fields["invoice"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
                "Placeholder": "Facturation",
            }
        )
        self.fields["delivery_key"].widget.attrs.update(
            {"class": "form-control mb-2 delivery-form", "Placeholder": "Numero de Livraison"}
        )
        self.fields["billing_status"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "mb-2 form-check-input delivery-form",
            }
        )
        self.fields["delivery_status"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "mb-2 form-check-input delivery-form",
            }
        )


class DeliveryDocumentsForm(UserDeliveryForm):
    document = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta(UserDeliveryForm.Meta):
        fields = UserDeliveryForm.Meta.fields + ["document"]


class OperationDetailForm(forms.ModelForm):

    durée = forms.DurationField(required=False)

    class Meta:
        model = OperationDetails
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
        widgets = {
            "delivery": forms.Select(attrs={"class": "form-control mb-3", "id": "form-delivery-details"}),
            "round": forms.Select(
                attrs={"class": "form-control mb-3", "placeholder": "delivery", "id": "form-delivery-details"}
            ),
            "distance": forms.NumberInput(attrs={"size": "10"}),
            "is_subcontract": forms.CheckboxInput(),
            "subcontractor": forms.Select(
                attrs={"class": "form-control mb-3", "placeholder": "delivery", "id": "form-delivery-details"}
            ),
            "subcontract_price": forms.NumberInput(),
            "is_loader": forms.CheckboxInput(),
            "loader_price": forms.NumberInput(),
            "is_commission": forms.CheckboxInput(),
            "commission_coast": forms.NumberInput(),
            "is_driver_charges": forms.CheckboxInput(),
            "driver_charges_coast": forms.NumberInput(),
            "extra_time": forms.TimeInput(),
            "extra_time_coast": forms.NumberInput(),
            "delivery_price": forms.NumberInput(),
        }
        labels = {
            "delivery": "La Livraison numero",
            "round": "la Tourné",
            "distance": "Distance",
            "is_subcontract": "sous traité?",
            "subcontractor": "Sous Traitant",
            "subcontract_price": "Charge Sous Traitant",
            "is_loader": "Besoin d'homme pour chargement",
            "loader_price": "Charges de chargeur",
            "is_commission": "avec Commisiion",
            "commission_coast": "Valeur Commission",
            "is_driver_charges": "Charge Chauffeur",
            "driver_charges_coast": "Coût des Charges Chauffeur",
            "extra_time": "Durée ",
            "extra_time_coast": "Coût du temps suplementaire",
            "delivery_price": "Coût de Livraison Totale",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["round"].required = False
        self.fields["delivery_price"].required = True
        self.fields["is_subcontract"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
            }
        )
        self.fields["is_loader"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
            }
        )
        self.fields["is_commission"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
            }
        )
        self.fields["is_driver_charges"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
            }
        )
        self.fields["is_commission"].widget.attrs.update(
            {
                "type": "checkbox",
                "class": "form-check-input delivery-form",
            }
        )


class DeliveryListForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"
