from django import forms
from django.forms import inlineformset_factory

from .models import Service, Amount, Product


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

