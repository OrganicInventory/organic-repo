from django.contrib import admin
from .models import Product, Service, Appointment, Amount, Brand, Stock

# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


class ProductAdmin(admin.ModelAdmin):
    #prod = Product.objects.get(pk=1)
    #prod.update_quantity(4)
    #quant = prod.display_quantity()
    list_display = ['name', 'quantity', 'max_quantity', 'display_quantity', 'size', 'id']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name',]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['date', 'service', 'id']

class AmountAdmin(admin.ModelAdmin):
    #amt = Amount.objects.get(pk=1)
    #amt.subtract()
    list_display = ['amount', 'service', 'product']

class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'used', 'date', 'stocked']

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Stock, StockAdmin)
