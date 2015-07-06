from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Appointment, Service

# Create your views here.

class AllProductsView(ListView):
    model = Product
    context_object_name = 'all_products'
    queryset = Product.objects.all().order_by('name', 'size')
    template_name = 'all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AllAppointmentsView(ListView):
    model = Appointment
    context_object_name = 'all_appointments'
    queryset = Appointment.objects.all().order_by('date')
    template_name = 'all_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AllServicesView(ListView):
    model = Service
    context_object_name = 'all_services'
    queryset = Service.objects.all().order_by('appointment')
    template_name = 'all_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

