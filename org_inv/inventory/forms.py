from django import forms
from django.forms import inlineformset_factory
from django.forms.extras import SelectDateWidget

from .models import Service, Amount, Product, Appointment


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name',]


# class AmountForm(forms.ModelForm):
#     def __init__(self, request, *args, **kwargs):
#         user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = Product.objects.filter(user=user)
#
#     class Meta:
#         model = Amount
#         fields = ['amount', 'product', 'service',]

def make_amount_form(user):
    class AmountForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product'].queryset = Product.objects.filter(user=user)

        class Meta:
            model = Amount
            fields = ['amount', 'product', 'service',]

    return AmountForm


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
    product = forms.ModelChoiceField(queryset=Product.objects.filter())
    amount_used = forms.FloatField(label='Amount Used (oz.)')


class ProductLookupForm(forms.Form):
    upc = forms.CharField(label='UPC Code')

    class Meta:
        fields = ['upc']
