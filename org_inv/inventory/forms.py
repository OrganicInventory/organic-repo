from django import forms
from django.forms import inlineformset_factory
from django.forms.extras import SelectDateWidget

from .models import Service, Amount, Product, Appointment


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name',]


class AmountForm(forms.ModelForm):
    class Meta:
        model = Amount
        fields = ['amount', 'product', 'service',]


AmountFormSet = inlineformset_factory(Service, Amount, fields=('product', 'amount'), can_delete=False)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'size', 'quantity']
        labels = {
            'size': 'Size (oz)',
            'quantity': "Quantity (units)"
        }


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget)
    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="Pick a Service", label='')

    class Meta:
        model = Appointment
        fields = ['date', 'service',]
