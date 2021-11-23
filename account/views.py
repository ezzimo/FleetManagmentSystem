from deliveries.models import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View, generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    ClientRegistrationForm,
    RegistrationForm,
    UserAddressForm,
    UserEditForm,
)
from .models import Address, Client, User
from .token import account_activation_token


@login_required
def dashboard(request):
    #    orders = user_orders(request) , {"orders": orders}
    return render(request, "account/dashboard/dashboard.html")


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = User.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


def account_register(request):

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password1"])
            user.is_active = False
            user.is_staff = False
            user.save()
            # Setup confirmation's email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            messages.success(request, "Creation du Compte réussi")
            return redirect("account:register_email_confirm")
    else:
        registerForm = RegistrationForm
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return request(request, "account/registration/activate_invalid.html")


@login_required
def add_client(request):

    if request.method == "POST":
        registerForm = ClientRegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.is_active = True
            user.save()
            messages.success(request, "Client Ajouter avec succé")
            return redirect("account:add_client_confirm")
    else:
        registerForm = ClientRegistrationForm
    return render(request, "account/registration/add_client.html", {"form": registerForm})


@login_required
def delete_client(request, id):
    client = Client.objects.get(pk=id)
    client.is_active = False
    client.save()
    return redirect("account:delete_confirmation")


@login_required
def view_clients(request):
    context = {}
    clients = Client.objects.filter(is_active=True)
    addresses = Address.objects.filter(is_active=True)
    context["clients"] = clients
    context["addresses"] = addresses

    if request.method == "GET":
        form = ClientRegistrationForm()
        context["form"] = form
        return render(request, "account/registration/clients.html", context)

    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.is_active = True
            client.save()

            messages.success(request, "Nouveau Client Ajouter")
            return redirect("account:clients")
        else:
            messages.error(request, "Problem traitement de votre demande")
            return redirect("account:clients")

    return render(request, "account/registration/clients.html", context)


class ClientDetailleView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = UserAddressForm
    template_name = "account/registration/client_detail.html"
    success_url = "account:client-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, pk=self.kwargs["pk"])
        context["object"] = context["client"] = client
        addresses = Address.objects.filter(customer_id=self.kwargs["pk"])
        context["addresses"] = addresses
        deliveries = OperationDetails.objects.filter(delivery__user=client)
        context["deliveries"] = deliveries
        return context

    def form_valid(self, form):
        form.instance.customer_id = self.kwargs["pk"]
        return super().form_valid(form)


@login_required
def view_address(request, pk):
    addresses = Address.objects.filter(is_active=True, customer_id=pk)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.is_active = True
            address_form.save()
            return HttpResponseRedirect(reverse("account:dashboard"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id).update(is_active=False)
    # address = Address.objects.get(pk=id)
    # address.is_active = False
    # address.save()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    address = Address.objects.get(pk=id)
    client = address.customer
    Address.objects.filter(customer=client, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=client).update(default=True)
    return redirect("account:addresses")
