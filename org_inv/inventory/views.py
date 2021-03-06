from datetime import timedelta, datetime, date
import json
import math
import itertools

from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.views.generic.detail import BaseDetailView
from org_inv import settings
import re
from factual import Factual
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, View, TemplateView
from .models import Product, Appointment, Service, Amount, Brand, Stock
from .forms import ServiceForm, ProductForm, AppointmentForm, AdjustUsageForm, \
    AmountFormSet, ThresholdForm, ProductUpdateForm, ProductNoQuantityForm, IntervalForm


# Create your views here.


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


#######################################################################################################################

class DashboardView(View):
    def get(self, request, **kwargs):
        appointments = Appointment.objects.prefetch_related('service').filter(date=date.today(), user=request.user)
        appts = {}
        for appt in appointments:
            appts[appt.service] = appts.get(appt.service, 0)
            appts[appt.service] += 1
        low = inventory_check(request.user.profile.interval, request.user)
        data = get_all_usage_data(request)
        return render(request, "dash.html", {"appts": appts, 'low': low, 'data': data})


#######################################################################################################################

class IndexView(TemplateView):
    template_name = 'index.html'


#######################################################################################################################

class AllProductsView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'all_products'
    template_name = 'all_products.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user).order_by('name', 'size')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values_dict = inventory_check(14, self.request.user)
        amts = []
        prods = []
        for pair in values_dict.items():
            prods.append(pair[0])
            amts.append(pair[1][0])
        context['prods'] = prods
        context['pairs'] = list(zip(prods, amts))
        return context


#######################################################################################################################

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/products/'

    def get_initial(self):
        if self.request.GET.get('upc'):
            if get_product(self.request.GET.get('upc'))[0]:
                initial = json.loads(get_product(self.request.GET.get("upc"))[0])
                initial['upc_code'] = self.request.GET.get('upc')
                brand = initial['brand']
                if Brand.objects.filter(user=self.request.user).filter(name=brand):
                    initial['brand'] = Brand.objects.get(user=self.request.user, name=brand)
                else:
                    new_brand = Brand.objects.create(name=brand, user=self.request.user)
                    initial['brand'] = new_brand
                return initial
            else:
                initial = []
                return initial
        else:
            return super().get_initial()

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.url = get_product(form.instance.upc_code)[1]
        form.instance.new_product_quantity(form.instance.quantity)
        form.instance.max_quantity = (form.instance.max_quantity * form.instance.size)
        form.instance.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "{} added.".format(form.instance.name))

        return super().form_valid(form)


#######################################################################################################################

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductNoQuantityForm
    template_name = 'product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Product.objects.get(upc_code=request.GET.get('upc'))
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
            return form_class(self.request, **self.get_form_kwargs())

    def get_initial(self):
        return {'max_quantity': self.object.display_max_quantity}

    def get_success_url(self):
        return reverse('all_products')

    def get_object(self, queryset=None, **kwargs):
        prod = Product.objects.get(upc_code=self.request.GET.get('upc'))
        return prod

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.max_quantity = float(form.data['max_quantity']) * self.object.size
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Product updated")
        return super().form_valid(form)


#######################################################################################################################

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        return Product.objects.get(user=self.request.user, upc_code=self.request.GET['upc'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.quantity < .1 * self.object.max_quantity:
            context['img'] = 'css/1.png'
        elif self.object.quantity < .2 * self.object.max_quantity:
            context['img'] = 'css/2.png'
        elif self.object.quantity < .3 * self.object.max_quantity:
            context['img'] = 'css/3.png'
        elif self.object.quantity < .4 * self.object.max_quantity:
            context['img'] = 'css/4.png'
        elif self.object.quantity < .5 * self.object.max_quantity:
            context['img'] = 'css/5.png'
        elif self.object.quantity < .6 * self.object.max_quantity:
            context['img'] = 'css/6.png'
        elif self.object.quantity < .7 * self.object.max_quantity:
            context['img'] = 'css/7.png'
        elif self.object.quantity < .8 * self.object.max_quantity:
            context['img'] = 'css/8.png'
        elif self.object.quantity < .9 * self.object.max_quantity:
            context['img'] = 'css/9.png'
        else:
            context['img'] = 'css/10.png'

        context['data'] = get_usage_data(self.object.id)
        context['pic'] = self.object.url
        return context


#######################################################################################################################

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
        messages.add_message(self.request, messages.SUCCESS, "{} Deleted".format(self.object))
        return HttpResponseRedirect(success_url)


#######################################################################################################################

class AllAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'all_appointments'
    template_name = 'all_appointments.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Appointment.objects.filter(user=self.request.user).order_by('date')
        return queryset

    def get_context_data(self, **kwargs):
        events = []
        for appt in Appointment.objects.filter(user=self.request.user).prefetch_related('service').order_by('date'):
            events.append({'title': appt.service.name, 'start': str(appt.date),
                           'adjust_usage': reverse('adjust_usage', kwargs={'appt_id': appt.id}),
                           'appt_edit': reverse('update_appointment', kwargs={'app_id': appt.id}),
                           'appt_cancel': reverse('delete_appointment', kwargs={'app_id': appt.id})})
        context = super().get_context_data(**kwargs)
        context['events'] = events
        return context


#######################################################################################################################

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'add_appointment.html'
    success_url = '/appointments/new'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Appointment for {} created".format(form.instance.date))
        form.save()
        return super().form_valid(form)


#######################################################################################################################

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
            messages.add_message(self.request, messages.SUCCESS,
                                 "Appointment for {} Cancelled".format(self.get_object(date)))
        return super(AppointmentDelete, self).post(request, *args, **kwargs)


#######################################################################################################################

class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Appointment.objects.filter(pk=self.kwargs['app_id'])[0]
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def get_success_url(self):
        return reverse('all_appointments')

    def get_object(self, queryset=None, **kwargs):
        appt = Appointment.objects.get(id=self.kwargs['app_id'])
        return appt

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Appointment Updated.")
        return super().form_valid(form)


#######################################################################################################################

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


#######################################################################################################################

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
            data['amounts'].form.base_fields['product'].empty_label = 'Pick a Product'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        amounts = context['amounts']
        if amounts.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            amounts.instance = self.object
            messages.add_message(self.request, messages.SUCCESS,
                                 "{} Added.".format(self.object))
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


#######################################################################################################################

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
            messages.add_message(self.request, messages.SUCCESS,
                                 "{} Updated".format(self.object))
            amounts.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_services')


#######################################################################################################################

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


#######################################################################################################################

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'

    def get_object(self, queryset=None):
        return Service.objects.get(user=self.request.user, id=self.kwargs['serv_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = get_service_data(self.object.id)
        prods = list(self.object.products.all())
        amts = []
        for prod in prods:
            amt = Amount.objects.get(product=prod, service=self.object)
            amts.append(amt)
        context['prods'] = self.object.products.all()
        context['prods_amts'] = zip(prods, amts)
        return context


#######################################################################################################################

def inventory_check(daterange, user):
    appointments = Appointment.objects.filter(user=user).filter(date__gt=timezone.now()).filter(
        date__lte=timezone.now() + timedelta(days=daterange)).prefetch_related('service').order_by('date')
    product_dict = {}
    for product in Product.objects.filter(user=user):
        if product.quantity < ((user.profile.threshold * .01) * product.max_quantity):
            product_dict[product] = [product.quantity, date.today()]
        else:
            product_dict[product] = [product.quantity]

    appts = appointments.prefetch_related('service__products__amount_set')
    for appointment in appts:
        for product in appointment.service.products.all():
            amount = [amount for amount in product.amount_set.all() if amount.product == product]
            amount = amount[0]
            if len(product_dict[product]) == 2:
                product_dict[product][0] -= amount.amount
            else:
                quant = product_dict[product][0] - amount.amount
                if quant < ((user.profile.threshold * .01) * product.max_quantity):
                    product_dict[product][0] -= amount.amount
                    product_dict[product].append(appointment.date)
                else:
                    product_dict[product][0] -= amount.amount

    low_products = {}

    for key, value in product_dict.items():
        if len(value) == 2:
            low_products[key] = value
            low_products[key].append(
                math.ceil((((user.profile.threshold * .01) * key.max_quantity) - low_products[key][0]) / key.size))
    return low_products


#######################################################################################################################

class LowInventoryView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'low_products'
    template_name = 'low_products.html'

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user).order_by('name', 'size')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        daterange = self.request.GET.get('range')
        if daterange:
            low = inventory_check(int(daterange), self.request.user)
        else:
            daterange = self.request.user.profile.interval
            low = inventory_check(self.request.user.profile.interval, self.request.user)

        context['range'] = daterange
        context['low'] = low
        return context


#######################################################################################################################

class NewOrderView(View):
    def get(self, request, **kwargs):
        if self.request.GET.get('upc'):
            product = Product.objects.filter(user=self.request.user).get(upc_code=self.request.GET.get('upc'))
            form = ProductForm(request,
                               initial={'user': self.request.user, 'upc_code': product.upc_code, 'name': product.name,
                                        'size': product.size, 'brand': product.brand})
        else:
            form = ProductUpdateForm(request, initial={'user': self.request.user})
        return render(request, "new_order.html", {"form": form})

    def post(self, request, **kwargs):
        form = ProductForm(request, request.POST, initial={'user': self.request.user})
        if Product.objects.filter(upc_code=request.POST.get('upc_code'), user=request.user):
            prod_instance = Product.objects.get(upc_code=request.POST.get('upc_code'), user=request.user)
            prod_instance.update_quantity(float(request.POST.get('quantity')))
            prod_instance.ordered = False
            prod_instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Product Updated.")
            return redirect("/products/new_order")
        else:
            return render(request, "new_order.html", {"form": form})


#######################################################################################################################

class EmptyProductView(BaseDetailView):
    def dispatch(self, request, *args, **kwargs):
        prod = Product.objects.get(id=self.kwargs['prod_id'])
        prod.quantity = 0
        prod.save()
        amounts = Amount.objects.filter(product=prod)
        messages.add_message(self.request, messages.SUCCESS, "{} quantity set to 0.".format(prod.name))
        for amount in amounts:
            up_perc = .1 * amount.amount
            new_amt = amount.amount + up_perc
            amount.amount = new_amt
            amount.save()
        return redirect('/products/')
        # def get_object(self, request):
        #    return Product.objects.get()


#######################################################################################################################

class CloseShopView(View):
    def dispatch(self, request, *args, **kwargs):
        appts = Appointment.objects.filter(date__lte=datetime.today(), done=False, user=request.user).order_by('date')
        messages.add_message(self.request, messages.SUCCESS, "Shop Closed")
        for appt in appts:
            appt.done = True
            appt.save()
            service = appt.service
            for prod in service.products.all():
                stock = prod.quantity
                amt = Amount.objects.get(product=prod, service=service)
                if Stock.objects.filter(product=prod, date=appt.date):
                    obj = Stock.objects.get(product=prod, date=appt.date)
                    obj.used += amt.amount
                    obj.stocked = stock
                    obj.save()
                else:
                    amount_used = amt.amount
                    Stock.objects.create(product=prod, used=amount_used, stocked=stock, date=appt.date)
                prod.quantity -= amt.amount
                prod.save()
        return redirect('/low/')


#######################################################################################################################

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
        return {'quantity': round(self.object.display_quantity, 2)}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.new_product_quantity(float(self.request.POST['quantity']))
        amounts = Amount.objects.filter(product=self.object)
        for amount in amounts:
            down_perc = .1 * amount.amount
            new_amt = amount.amount - down_perc
            amount.amount = new_amt
            amount.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 "{} quantity adjusted.".format(self.object.name))
            return redirect('/products/')


#######################################################################################################################

class AdjustUsageView(View):
    def get(self, request, **kwargs):
        appt = Appointment.objects.get(id=self.kwargs['appt_id'])
        form = AdjustUsageForm(user=request.user, appointment=appt)
        if self.request.user == appt.user:
            return render(request, "adjust_usage.html", {'form': form, 'appt': appt})
        else:
            return HttpResponseForbidden()

    def post(self, request, **kwargs):
        appt = Appointment.objects.get(id=self.kwargs['appt_id'])
        form = AdjustUsageForm(request.POST, user=request.user, appointment=appt)
        if form.is_valid():
            amt = Amount.objects.get(product=form.data['product'], service=appt.service)
            diff = float(form.data['amount_used']) - amt.amount
            prod = Product.objects.get(id=form.data['product'])
            prod.quantity -= diff
            prod.save()
            return redirect('/products/')


#######################################################################################################################

class OrderView(View):
    def get(self, request, **kwargs):
        daterange = self.request.GET.get('range')
        if daterange != 'None':
            all_low = inventory_check(int(daterange), self.request.user)
            low = {}
            for product, value in all_low.items():
                if product.brand.email and not product.ordered:
                    low[product] = value
        else:
            all_low = inventory_check(self.request.user.profile.interval, self.request.user)
            low = {}
            for product, value in all_low.items():
                if not product.ordered:
                    low[product] = value
        return render(request, "order.html", {'products': low.items()})

    def post(self, request, *args, **kwargs):
        products = {Product.objects.get(user=request.user, upc_code=key): value for key, value in
                    self.request.POST.items() if key != 'csrfmiddlewaretoken'}
        brands = {key.brand for key in products.keys()}
        messages.add_message(self.request, messages.SUCCESS, "Order Sent")
        for brand in brands:
            brand_products = []
            message = "Hello from {}!\nWould you please order the following products for us:\n".format(
                request.user.profile.spa_name)
            send = False
            for key, value in products.items():
                if key.brand == brand and int(value) > 0:
                    key.ordered = True
                    key.save()
                    brand_products.append(key)
                    send = True
                    message += "{} (upc {}): {} unit(s)".format(key.name, key.upc_code, value) + "\n"
            if send:
                send_mail('Order from {} in {}'.format(request.user.profile.spa_name, request.user.profile.location),
                          message, settings.EMAIL_HOST_USER,
                          [brand.email], fail_silently=False)
        return redirect('/low/')


#######################################################################################################################

class SettingsView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        form = ThresholdForm()
        form2 = IntervalForm()
        brands = Brand.objects.filter(user=request.user).order_by('name')
        return render(request, 'settings.html', {'form': form, 'form2': form2, 'brands': brands})

    def post(self, request, **kwargs):
        form = ThresholdForm(request.POST)
        form2 = IntervalForm(request.POST)
        if request.POST.get('thresh-submit') == '':
            if form.is_valid():
                amt = form.data['percent']
                prof = request.user.profile
                prof.threshold = amt
                messages.add_message(self.request, messages.SUCCESS,
                                     "Threshold updated to {}%.".format(amt))
                prof.save()
        else:
            if form2.is_valid():
                interval = form2.data['interval']
                prof = request.user.profile
                prof.interval = interval
                messages.add_message(self.request, messages.SUCCESS,
                                     "Interval updated to {}.".format(interval))
                prof.save()
        return redirect('/settings/')


#######################################################################################################################

class EmailUpdate(LoginRequiredMixin, UpdateView):
    model = Brand
    fields = ['name', 'email']
    template_name = 'update_email.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Brand.objects.get(pk=self.kwargs['brand_id'])
        if self.request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)

        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('settings')

    def get_object(self, queryset=None, **kwargs):
        brand = Brand.objects.get(id=self.kwargs['brand_id'])
        return brand

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


#######################################################################################################################

class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    fields = ['name', 'email']
    template_name = 'create_brand.html'
    success_url = '/settings/'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)


#######################################################################################################################

def get_prod_data(request):
    products = Product.objects.filter(user=request.user).prefetch_related('stock_set').order_by('name')
    data = []
    enabled = True
    for product in products:
        stocks = product.stock_set.all()
        if stocks:
            dates = sorted([stock.date for stock in stocks])
            date_set = set(dates[0] + timedelta(x) for x in range((dates[-1] - dates[0]).days))
        else:
            date_set = {}
        values = []
        aggregate = []
        usages = {}
        for date in sorted(date_set):
            usages[str(date)] = 0
            date_stocks = [stock for stock in stocks if stock.date == date]
            for stock in date_stocks:
                usages[str(stock.date)] = stock.used
        for key, value in sorted(usages.items(), key=lambda x: x[0]):
            aggregate.append((key, value))

        def to_week(day_data):
            sunday = datetime.strptime(str(day_data[0]), '%Y-%m-%d').strftime('%Y-%U-0')
            return datetime.strptime(sunday, '%Y-%U-%w').strftime('%Y-%m-%d')

        weekly = itertools.groupby(aggregate, to_week)

        aggregate_weekly = (
            (week, sum(day_usages for date, day_usages in usages))
            for week, usages in weekly)
        for week, value in aggregate_weekly:
            values.append({'x': datetime.strptime(week, "%Y-%m-%d").timestamp(), 'y': value})
        if enabled:
            data.append({'values': values, 'key': product.name})
            enabled = False
        else:
            data.append({'values': values, 'key': product.name, 'disabled': 'True'})
    return data


#######################################################################################################################

def get_service_data(serv_id):
    service = Service.objects.get(id=serv_id)
    appts = Appointment.objects.filter(service=service, date__lte=datetime.today(),
                                  date__gte=(datetime.today() - timedelta(days=31)))
    if appts:
        dates = sorted([appt.date for appt in appts])
        date_set = set(dates[0] + timedelta(x) for x in range((dates[-1] - dates[0]).days))
    else:
        date_set = {}
    values = []
    usages = {}
    for date in sorted(date_set):
        usages[str(date)] = 0
        date_appts = [appt for appt in appts if appt.date == date]
        for appt in date_appts:
            appt_date = str(appt.date)
            if appt_date in usages.keys():
                usages[appt_date] += 1
            else:
                usages[appt_date] = 1
    for key, value in sorted(usages.items(), key=lambda x: x[0]):
        values.append({'x': datetime.strptime(key, "%Y-%m-%d").timestamp(), 'y': value})
    data = []
    data.append({'values': values, 'key': 'number of appointments', 'area': 'True'})
    return data

#######################################################################################################################

def get_all_service_data(request):
    services = Service.objects.filter(user=request.user).order_by('name')
    data = []
    enabled = True
    for service in services:
        appts = Appointment.objects.filter(service=service).order_by('date')
        if appts:
            dates = sorted([appt.date for appt in appts])
            date_set = set(dates[0] + timedelta(x) for x in range((dates[-1] - dates[0]).days))
        else:
            date_set = {}
        values = []
        aggregate = []
        usages = {}
        for date in sorted(date_set):
            usages[str(date)] = 0
            date_appts = [appt for appt in appts if appt.date == date]
            for appt in date_appts:
                appt_date = str(appt.date)
                if appt_date in usages.keys():
                    usages[appt_date] += 1
                else:
                    usages[appt_date] = 1
        for key, value in sorted(usages.items(), key=lambda x: x[0]):
            aggregate.append((key, value))

        def to_week(day_data):
            sunday = datetime.strptime(str(day_data[0]), '%Y-%m-%d').strftime('%Y-%U-0')
            return datetime.strptime(sunday, '%Y-%U-%w').strftime('%Y-%m-%d')

        weekly = itertools.groupby(aggregate, to_week)

        aggregate_weekly = (
            (week, sum(day_usages for date, day_usages in usages))
            for week, usages in weekly)
        for week, value in aggregate_weekly:
            values.append({'x': datetime.strptime(week, "%Y-%m-%d").timestamp(), 'y': value})
        if enabled:
            data.append({'values': values, 'key': service.name})
            enabled = False
        else:
            data.append({'values': values, 'key': service.name, 'disabled': 'True'})
    return data


#######################################################################################################################

def get_product(upc_code):
    factual = Factual("gCKclwfy6eBki5UyHDxS56x7zmcvCMaGJ7l7v9cM", "Dt8V4ngb484Blmyaw5G9SxbycgpOsJL0ENckwxX0")
    products = factual.table('products')
    data = products.filters({'upc': {'$includes': upc_code}}).data()
    if data:
        upc_data = data[0]
        wanted = ['size', 'product_name', 'brand', 'image_urls']
        new = {}
        for pair in upc_data.items():
            if pair[0] in wanted:
                if pair[0] == 'product_name':
                    new['name'] = pair[1]
                elif pair[0] == 'size':
                    new['size'] = float(re.search(r'[\d\.]+', pair[1][0]).group())
                elif pair[0] == 'image_urls':
                    new['pic'] = pair[1][0]
                else:
                    new[pair[0]] = pair[1]
        new_json = json.dumps(new)
        return new_json, new['pic']
    else:
        return None, None


#######################################################################################################################

def get_usage_data(prod_id):
    prod = Product.objects.get(pk=prod_id)
    stocks = Stock.objects.filter(product=prod, date__lte=datetime.today(),
                                  date__gte=(datetime.today() - timedelta(days=365))).order_by('date')
    usage_values = []
    stock_values = []
    for stock in stocks:
        usage_values.append({'x': datetime.strptime(str(stock.date), "%Y-%m-%d").timestamp(), 'y': stock.used})
        stock_values.append({'x': datetime.strptime(str(stock.date), "%Y-%m-%d").timestamp(), 'y': stock.stocked})
    data1 = []
    data1.append({'values': usage_values, 'key': 'product usage (oz)', 'area': 'True'})
    data1.append({'values': stock_values, 'key': 'product in stock (oz)', 'area': 'True'})
    return data1

#######################################################################################################################

def get_all_usage_data(request):
    products = Product.objects.filter(user=request.user).prefetch_related(
        Prefetch("stock_set", queryset=Stock.objects.filter(date__lte=datetime.today(),
                                                            date__gte=(datetime.today() - timedelta(days=91))).order_by(
            'date'), to_attr="stocks")).order_by('name')
    data = []
    enabled = True
    for product in products:
        stocks = [stock for stock in product.stocks if stock.product == product]
        if stocks:
            initial = stocks[0].stocked
        else:
            initial = product.quantity
        days = list((date.today() - timedelta(days=91)) + timedelta(x) for x in
                    range((date.today() - (date.today() - timedelta(days=91))).days))
        sundays = [day for day in days if day.isocalendar()[2] == 7]
        values = []
        usages = {}
        for sunday in sundays:
            stock = [stock for stock in stocks if stock.date <= sunday]
            if stock:
                day = str(sunday)
                usages[day] = usages.get(day, 0)
                usages[day] += stock[-1].stocked
                initial = stock[-1].stocked
            else:
                day = str(sunday)
                usages[day] = usages.get(day, 0)
                usages[day] += initial
        for key, value in sorted(usages.items(), key=lambda x: x[0]):
            values.append({'x': datetime.strptime(str(key), "%Y-%m-%d").timestamp(), 'y': value})
        if enabled:
            data.append({'values': values, 'key': product.name, 'area': 'True'})
            enabled = False
        else:
            data.append({'values': values, 'key': product.name, 'disabled': 'True', 'area': 'True'})
    return data


#######################################################################################################################

def search_bar(request):
    query = request.GET.get('upc')
    if query:
        results = Product.objects.filter(user=request.user, name__icontains=request.GET['upc'])
    else:
        results = Product.objects.all()
    return render(request, 'search_results.html', {'results': results})
