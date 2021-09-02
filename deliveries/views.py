from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Delivery, DeliveryDetails, Round, Subcontractor


class DeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
    template_name = "deliveries/customer/edit_deliveries.html"
    success_url = reverse_lazy("account:dashboard")

    def test_func(self):
        return self.request.user.is_customer and self.request.user.is_active

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
