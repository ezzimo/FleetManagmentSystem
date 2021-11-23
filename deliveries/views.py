from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import DeliveryListForm, OperationDetailForm, UserDeliveryForm
from .models import Delivery, OperationDetails, Round, Subcontractor


class DeliveryListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Delivery
    form_class = DeliveryListForm
    template_name = "deliveries/customer/deliveries.html"
    success_url = reverse_lazy("account:dashboard")

    def test_func(self):
        return self.request.user.user_type == "ad" and self.request.user.is_active


class DeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, FormView):
    model = Delivery
    form_class = UserDeliveryForm
    template_name = "deliveries/customer/edit_deliveries.html"

    def get_success_url(self):
        return reverse("delivery:operation-form", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_active

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("decument")
        if form.is_valid():
            for file in files:
                self.Delivery.objects.create(document=file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def form_valid(self, form):
    #     form.instance.user_id = self.request.user.id
    #     return super().form_valid(form)


class DeliveryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Delivery
    template_name = "deliveries/operator/delivery_details.html"

    def get_success_url(self):
        return reverse("delivery:operation-form", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_active


class DeliveryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Delivery
    form_class = UserDeliveryForm
    template_name = "deliveries/customer/edit_deliveries.html"

    def test_func(self):
        return self.request.user.is_active


class DeliveryDeleteeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Delivery
    template_name = "deliveries/customer/delete_delivery.html"
    success_url = reverse_lazy("delivery:deliveries")

    def test_func(self):
        return self.request.user.is_active


class OperationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, FormView):
    model = OperationDetails
    form_class = OperationDetailForm
    template_name = "deliveries/responsable/edit_operation_details.html"
    success_url = reverse_lazy("account:dashboard")

    # def get_success_url(self):
    # return reverse("account:dashboard", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_active

    def get_initial(self):
        initial = super(OperationCreateView, self).get_initial()
        initial = initial.copy()
        delivery = get_object_or_404(Delivery, pk=self.kwargs["pk"])
        distance = delivery.google_distance_value
        duration = delivery.google_duration_value
        initial["delivery"] = delivery
        initial["distance"] = distance
        initial["durée"] = duration
        return initial

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(self.kwargs)
    #     delivery = Delivery.objects.filter(id=self.kwargs["pk"])
    #     context["form"].fields["delivery"].queryset = delivery
    #     print(delivery)
    #     distance = Delivery.objects.get(id=self.kwargs["pk"]).distance["google_distance"]
    #     print("distance: " + distance)
    #     self.kwargs = {"distance": distance}
    #     context["form"].fields["distance"].queryset = distance
    #     print(context["form"].fields["distance"].queryset)
    #     return contextclass DeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, FormView):


class OperationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = OperationDetails
    template_name = "deliveries/responsable/detail_deliveries_details.html"

    def test_func(self):
        return self.request.user.is_active
