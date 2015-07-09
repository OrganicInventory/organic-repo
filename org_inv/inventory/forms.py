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
    quantity = forms.FloatField(initial="", label="Quantity (units)")

    class Meta:
        model = Product
        fields = ['name', 'size', 'quantity', 'upc_code']
        labels = {
            'size': 'Size (oz)'
        }


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Appointment
        fields = ['date', 'service',]


class AdjustUsageForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    amount_used = forms.FloatField(label='Amount Used (oz.)')


class ProductLookupForm(forms.Form):
    upc = forms.CharField(label='UPC Code')

    class Meta:
        fields = ['upc']
