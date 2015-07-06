from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.

class AllProductsView(ListView):
    model = Product
    context_object_name = 'all_products'
    queryset = Product.objects.all().order_by('name', 'size')
    template_name = 'all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


