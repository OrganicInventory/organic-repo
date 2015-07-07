from datetime import timedelta

from django.utils import timezone
from django.views.generic import ListView, CreateView
from .models import Product, Appointment, Service, Amount

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


class AllServicesView(ListView):
    model = Service
    context_object_name = 'all_services'
    queryset = Service.objects.all().order_by('appointment')
    template_name = 'all_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
