from datetime import timedelta

from django.utils import timezone
from django.views.generic import ListView
from .models import Product, Appointment, Amount


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
