from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import (
    AnssuranceCompany,
    AnssuranceType,
    Make,
    ModelSpecificationValue,
    Vehicle,
    VehicleModel,
)


def vehicle_all(request):
    vehicles = Vehicle.objects.prefetch_related("model")
    return render(request, "vehicle/index.html", {"vehicles": vehicles})


def vehicle_detail(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    specifications = ModelSpecificationValue.objects.filter(vehicle=vehicle)
    return render(request, "vehicle/vehicle.html", {"vehicle": vehicle, "specifications": specifications})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug.capitalize()).get_descendants(include_self=True)
    )
    return render(request, "ecommerce_store/category.html", {"category": category, "products": products})


######################################################################################
#######################   Vehicle Model        ######################################
######################################################################################


class VehicleCreationView(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = "__all__"
    success_url = reverse_lazy("vehicle:vehicles_all")


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    fields = "__all__"
    success_url = reverse_lazy("vehicle:vehicles_all")


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    fields = "__all__"
    success_url = reverse_lazy("vehicle:vehicles_all")
