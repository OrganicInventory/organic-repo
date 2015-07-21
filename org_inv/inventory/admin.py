from django.contrib import admin
from .models import Product, Service, Appointment, Amount, Brand, Stock

# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'max_quantity', 'display_max_quantity', 'display_quantity', 'size', 'id', 'user']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name',]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['date', 'service', 'id', 'done']

class AmountAdmin(admin.ModelAdmin):
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
