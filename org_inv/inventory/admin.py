from django.contrib import admin
from .models import Product, Service, Appointment

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'size',]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name',]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['date', 'service',]

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
