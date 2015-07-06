from django.db import models
import datetime

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    size = models.IntegerField()

    def update_quantity(self, quantity_entered):
        add_this = quantity_entered * self.size
        updated = self.quantity + add_this
        self.quantity = updated
        self.save()

    def display_quantity(self):
        return self.quantity / self.size

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    date = models.DateField()
    service = models.ForeignKey(Service)

    def __str__(self):
        return "{}: {}".format(self.service, self.date)


class Amount(models.Model):
    amount = models.FloatField()
    product = models.ForeignKey(Product)
    service = models.ForeignKey(Service)

    def __str__(self):
        return self.amount

