from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField(default=0)
    max_quantity = models.FloatField(default=0, null=True, blank=True)
    size = models.FloatField()
    user = models.ForeignKey(User, null=True)
    brand = models.ForeignKey(Brand, null=True)
    upc_code = models.CharField(max_length=100, null=True)
    url = models.CharField(null=True, max_length=255)

    class Meta:
        unique_together = ('name', 'size', 'user')

    @property
    def display_quantity(self):
        return self.quantity / self.size

    @property
    def display_max_quantity(self):
        return self.max_quantity / self.size

    def new_product_quantity(self, quantity_entered):
        self.quantity = quantity_entered * self.size
        self.save()

    def update_quantity(self, quantity_entered):
        add_this = quantity_entered * self.size
        updated = self.quantity + add_this
        self.quantity = updated
        self.save()

    def __str__(self):
        return "{}:{}".format(self.name, self.size)


class Amount(models.Model):
    amount = models.FloatField()
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey('Service', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.amount)

    def subtract(self):
        new_quant = self.product.quantity - self.amount
        self.product.quantity = new_quant
        self.product.save()

    def calculate(self):
        return self.product.quantity - self.amount


class Service(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through=Amount)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    date = models.DateField()
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.service, self.date)


class Stock(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    used = models.FloatField()
    stocked = models.FloatField()


