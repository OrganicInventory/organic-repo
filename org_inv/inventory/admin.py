from django.contrib import admin
from .models import Product, Service, Appointment, Amount

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    #prod = Product.objects.get(pk=1)
    #prod.update_quantity(4)
    #quant = prod.display_quantity()
    list_display = ['name', 'quantity', 'max_quantity', 'display_quantity', 'size',]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name',]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['date', 'service', 'id']

class AmountAdmin(admin.ModelAdmin):
    #amt = Amount.objects.get(pk=1)
    #amt.subtract()
    list_display = ['amount', 'service', 'product']

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Amount, AmountAdmin)
