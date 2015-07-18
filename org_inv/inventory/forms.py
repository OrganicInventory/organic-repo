from django import forms
from django.forms import inlineformset_factory
from django.forms.extras import SelectDateWidget

from .models import Service, Amount, Product, Appointment, Brand


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name',]

AmountFormSet = inlineformset_factory(Service, Amount, fields=['product', 'amount'], can_delete=False)


class ProductForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(user=request.user)

    quantity = forms.FloatField(initial="", label="Quantity (units)")
    max_quantity = forms.FloatField(initial="", label="Max Quantity (when fully stocked)")
    # brand = forms.CharField(max_length=255)

    class Meta:
        model = Product
        fields = ['name', 'brand', 'size', 'quantity', 'max_quantity', 'upc_code']
        labels = {
            'size': 'Size (oz)',
            'brand': ''
        }


class ProductUpdateForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['brand'].queryset = Brand.objects.filter(user=request.user)

    upc_code = forms.CharField(initial="", label="UPC Code")
    quantity = forms.FloatField(initial="", label="Quantity (units)")
    max_quantity = forms.FloatField(initial="", label="Max Quantity (when fully stocked)")
    name = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    brand = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    size = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    # brand = forms.CharField(max_length=255)

    class Meta:
        model = Product
        fields = ['upc_code', 'quantity', 'name', 'brand', 'size']
        labels = {'brand': '', 'name': '', 'size': ''}


class ProductNoQuantityForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(user=request.user)

    upc_code = forms.CharField(initial="", label="UPC Code")
    quantity = forms.FloatField(initial="", widget=forms.HiddenInput(), required=False)
    # brand = forms.CharField(max_length=255)

    class Meta:
        model = Product
        fields = ['upc_code', 'quantity', 'name', 'brand', 'size']
        labels = {'brand': '', 'name': 'Name', 'size': 'Size (oz)'}


class ThresholdForm(forms.Form):
    percent = forms.IntegerField(label='Enter New Threshold')

    class Meta:
        fields = ['percent']


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
        appointment = kwargs.pop('appointment')
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(user=user, amount__service__appointment=appointment)


class ProductLookupForm(forms.Form):
    upc = forms.CharField(label='UPC Code')

    class Meta:
        fields = ['upc']


class OrderForm(forms.Form):
    number = forms.IntegerField()

    class Meta:
        fields = ['number']
