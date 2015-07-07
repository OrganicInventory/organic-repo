from datetime import timedelta
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Product, Appointment, Service, Amount
from .forms import ServiceForm, AmountForm, AmountFormSet

# Create your views here.

class AllProductsView(ListView):
    model = Product
    context_object_name = 'all_products'
    queryset = Product.objects.all().order_by('name', 'size')
    template_name = 'all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'size', 'quantity']
    template_name = 'create_product.html'
    success_url = '/products/'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.update_max_quantity()
        return super().form_valid(form)


class AllAppointmentsView(ListView):
    model = Appointment
    context_object_name = 'all_appointments'
    queryset = Appointment.objects.all().order_by('date')
    template_name = 'all_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AppointmentCreateView(CreateView):
    model = Appointment
    fields = ['date', 'service']
    template_name = 'add_appointment.html'
    success_url = '/appointments/'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        return super().form_valid(form)


class AppointmentDelete(DeleteView):
    model = Appointment

    def get_success_url(self):
        return reverse('all_appointments')

    def get_object(self, queryset=None):
        return Appointment.objects.filter(pk=self.kwargs['app_id'])[0]

    def get_template_names(self):
        return 'appointment_confirm_delete.html'


class AppointmentUpdate(UpdateView):
    model = Appointment
    fields = ['date', 'service']
    template_name = 'appointment_update_form.html'

    def get_success_url(self):
        return reverse('all_appointments')

    def get_object(self, queryset=None, **kwargs):
        appt = Appointment.objects.get(id=self.kwargs['app_id'])
        return appt

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AllServicesView(ListView):
    model = Service
    context_object_name = 'all_services'
    queryset = Service.objects.all().order_by('appointment')
    template_name = 'all_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'create_service.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['amounts'] = AmountFormSet(self.request.POST)
        else:
            data['amounts'] = AmountFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        amounts = context['amounts']
        # with transaction.commit_on_success():
        if amounts.is_valid():
            self.object = form.save()
            amounts.instance = self.object
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


class ServiceUpdate(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_update_form.html'

    def get_object(self, queryset=None, **kwargs):
        serv = Service.objects.get(id=self.kwargs['serv_id'])
        return serv

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['amounts'] = AmountFormSet(self.request.POST, instance=self.object)
        else:
            data['amounts'] = AmountFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        amounts = context['amounts']
        # with transaction.commit_on_success():
        if amounts.is_valid():
            amounts.instance = self.object
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


# class ServiceUpdate(UpdateView):
#     model = Service
#     form_class = ServiceForm
#     template_name = 'service_update_form.html'
#
#     def get_success_url(self):
#         return reverse('all_appointments')
#
#     def get_object(self, queryset=None, **kwargs):
#         appt = Appointment.objects.get(id=self.kwargs['app_id'])
#         return appt
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return super().form_valid(form)


def inventory_check(daterange):
    appointments = Appointment.objects.filter(date__gt=timezone.now()).filter(
        date__lte=timezone.now() + timedelta(days=daterange))
    product_dict = {}
    for product in Product.objects.all():
        product_dict[product] = product.quantity

    for appointment in appointments:
        for product in appointment.service.products.all():
            amount = Amount.objects.get(product=product, service=appointment.service)
            product_dict[product] -= amount.amount

    low_products = {}

    for key, value in product_dict.items():
        if value < (.3 * key.max_quantity):
            low_products[key] = value

    return low_products
