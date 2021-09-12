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
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import DeliveryDetailsForm, UserDeliveryForm
from .models import Delivery, DeliveryDetails, Round, Subcontractor


class DeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, FormView):
    model = Delivery
    form_class = UserDeliveryForm
    template_name = "deliveries/customer/edit_deliveries.html"
    success_url = reverse_lazy("account:dashboard")

    def test_func(self):
        return self.request.user.user_type == "ad" and self.request.user.is_active

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("decument")
        if form.is_valid():
            for f in files:
                self.model.objects.create(document=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class DetailsDeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, FormView):
    model = DeliveryDetails
    form_class = DeliveryDetailsForm
    template_name = "deliveries/responsable/edit_deliveries_details.html"
    success_url = reverse_lazy("account:dashboard")

    def test_func(self):
        return self.request.user.is_responsable and self.request.user.is_active

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
