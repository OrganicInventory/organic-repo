from django import forms
from django.forms import inlineformset_factory
from django.forms.extras import SelectDateWidget

from .models import Service, Amount, Product, Appointment


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name',]

AmountFormSet = inlineformset_factory(Service, Amount, fields=['product', 'amount'], can_delete=False)


class ProductForm(forms.ModelForm):
    quantity = forms.FloatField(initial="", label="Quantity (units)")

    class Meta:
        model = Product
        fields = ['name', 'size', 'quantity', 'upc_code']
        labels = {
            'size': 'Size (oz)'
        }


class AppointmentForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(user=request.user)
        self.fields['service'].empty_label = "Pick a Service"

    class Meta:
        model = Appointment
        fields = ['date', 'service',]
        labels = {
            'date': '',
            'service': ''
        }
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'})
        }


class AdjustUsageForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    amount_used = forms.FloatField(label='Amount Used (oz.)')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(user=user)


class ProductLookupForm(forms.Form):
    upc = forms.CharField(label='UPC Code')

    class Meta:
        fields = ['upc']
