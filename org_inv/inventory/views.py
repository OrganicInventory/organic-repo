from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, View, TemplateView
from .models import Product, Appointment, Service, Amount
from functools import partial, wraps
from .forms import ServiceForm, ProductForm, AppointmentForm, AdjustUsageForm, \
    ProductLookupForm, make_amount_form, AmountFormSet

# Create your views here.


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'index.html'


class AllProductsView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'all_products'
    template_name = 'all_products.html'

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user).order_by('name', 'size')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/products/'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.new_product_quantity(form.instance.quantity)
        form.instance.update_max_quantity()
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        return Product.objects.filter(user=self.request.user).filter(upc_code=self.request.GET['upc'])[0]


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ProductDeleteView, self).post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        obj = Product.objects.filter(id=self.kwargs['prod_id'])[0]
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('all_products')

    def get_object(self, queryset=None):
        prod = Product.objects.get(pk=self.kwargs['prod_id'])
        return prod

    def get_template_names(self):
        return 'product_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['affected_services'] = self.object.service_set.all()
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        Amount.objects.filter(product=self.object).delete()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class AllAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'all_appointments'
    template_name = 'all_appointments.html'

    def get_queryset(self):
        queryset = Appointment.objects.filter(user=self.request.user).order_by('date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'add_appointment.html'
    success_url = '/appointments/'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        return super().form_valid(form)


class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment

    def dispatch(self, request, *args, **kwargs):
        obj = Appointment.objects.filter(pk=self.kwargs['app_id'])[0]
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('all_appointments')

    def get_object(self, queryset=None):
        return Appointment.objects.filter(pk=self.kwargs['app_id'])[0]

    def get_template_names(self):
        return 'appointment_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(AppointmentDelete, self).post(request, *args, **kwargs)


class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['date', 'service']
    template_name = 'appointment_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Appointment.objects.filter(pk=self.kwargs['app_id'])[0]
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('all_appointments')

    def get_object(self, queryset=None, **kwargs):
        appt = Appointment.objects.get(id=self.kwargs['app_id'])
        return appt

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AllServicesView(LoginRequiredMixin, ListView):
    model = Service
    context_object_name = 'all_services'
    template_name = 'all_services.html'

    def get_queryset(self):
        queryset = Service.objects.filter(user=self.request.user).order_by('name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'create_service.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['amounts'] = AmountFormSet(self.request.POST)
        else:
            data['amounts'] = AmountFormSet()
            data['amounts'].form.base_fields['product'].queryset = Product.objects.filter(user=self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        amounts = context['amounts']
        if amounts.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            amounts.instance = self.object
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


class ServiceUpdate(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Service.objects.get(id=self.kwargs['serv_id'])
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_object(self, queryset=None, **kwargs):
        serv = Service.objects.get(id=self.kwargs['serv_id'])
        return serv

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['amounts'] = AmountFormSet(self.request.POST, instance=self.object)
        else:
            data['amounts'] = AmountFormSet(instance=self.object)
            data['amounts'].form.base_fields['product'].queryset = Product.objects.filter(user=self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        amounts = context['amounts']
        if amounts.is_valid():
            amounts.instance = self.object
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


class ServiceDelete(LoginRequiredMixin, DeleteView):
    model = Service

    def dispatch(self, request, *args, **kwargs):
        obj = Service.objects.get(id=self.kwargs['serv_id'])
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('all_services')

    def get_object(self, queryset=None):
        serv = Service.objects.get(pk=self.kwargs['serv_id'])
        return serv

    def get_template_names(self):
        return 'service_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ServiceDelete, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        Amount.objects.filter(service=self.object).delete()
        Appointment.objects.filter(service=self.object).delete()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def inventory_check(daterange, user):
    appointments = Appointment.objects.filter(user=user).filter(date__gt=timezone.now()).filter(
        date__lte=timezone.now() + timedelta(days=daterange))
    product_dict = {}
    for product in Product.objects.filter(user=user):
        product_dict[product] = product.quantity

    for appointment in appointments:
        for product in appointment.service.products.all():
            amount = Amount.objects.get(product=product, service=appointment.service)
            product_dict[product] -= amount.amount

    low_products = {}

    for key, value in product_dict.items():
        if value < (.3 * key.max_quantity):
            low_products[key] = value

    return low_products


class LowInventoryView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'low_products'
    template_name = 'low_products.html'

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user).order_by('name', 'size')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        low = inventory_check(14, self.request.user)
        context['low'] = low
        return context


class NewOrderView(View):
    def get(self, request, **kwargs):
        form = ProductForm(initial={'user': self.request.user})
        return render(request, "new_order.html", {"form": form})

    def post(self, request, **kwargs):
        form = ProductForm(request.POST, initial={'user': self.request.user})
        if Product.objects.filter(name=request.POST.get('name'), size=float(request.POST.get('size'))).filter(user=request.user):
            prod_instance = Product.objects.filter(name=request.POST.get('name'), size=float(request.POST.get('size')))[0]
            prod_instance.update_quantity(float(request.POST.get('quantity')))
            prod_instance.update_max_quantity()
            prod_instance.save()
            return redirect("/products/")
        else:
            return render(request, "new_order.html", {"form": form})


class EmptyProductView(View):
    def dispatch(self, request, *args, **kwargs):
        prod = Product.objects.get(id=self.kwargs['prod_id'])
        prod.quantity = 0
        prod.save()
        amounts = Amount.objects.filter(product=prod)
        for amount in amounts:
            up_perc = .1 * amount.amount
            new_amt = amount.amount + up_perc
            amount.amount = new_amt
            amount.save()
        return redirect('/products/')


class TooMuchProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['quantity']
    template_name = "adjust_product.html"

    def dispatch(self, request, *args, **kwargs):
        obj = Product.objects.filter(pk=self.kwargs['prod_id'])[0]
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_queryset(self):
        prod = Product.objects.filter(id=self.kwargs['prod_id'])
        return prod

    def get_success_url(self):
        return reverse('all_products')

    def get_object(self, queryset=None, **kwargs):
        prod = Product.objects.get(id=self.kwargs['prod_id'])
        return prod

    def get_initial(self):
        return {'quantity': self.object.display_quantity}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.new_product_quantity(float(self.request.POST['quantity']))
        amounts = Amount.objects.filter(product=self.object)
        for amount in amounts:
            down_perc = .1 * amount.amount
            new_amt = amount.amount - down_perc
            amount.amount = new_amt
            amount.save()
        return redirect('/products/')


class AdjustUsageView(View):
    def get(self, request, **kwargs):
        form = AdjustUsageForm(user=request.user)
        appt = Appointment.objects.get(id=self.kwargs['appt_id'])
        if self.request.user == appt.user:
            return render(request, "adjust_usage.html", {'form': form, 'appt': appt})
        else:
            return HttpResponseForbidden()

    def post(self, request, **kwargs):
        form = AdjustUsageForm(request.POST, user=request.user)
        appt = Appointment.objects.get(id=self.kwargs['appt_id'])
        if form.is_valid():
            amt = Amount.objects.get(product=form.data['product'], service=appt.service)
            diff = int(form.data['amount_used']) - amt.amount
            prod = Product.objects.get(id=form.data['product'])
            prod.quantity -= diff
            prod.save()
        return redirect('/products/')
