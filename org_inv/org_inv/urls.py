"""org_inv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import inventory.views as inv_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^products/$', inv_views.AllProductsView.as_view(), name="all_products"),
    url(r'^low/$', inv_views.LowInventoryView.as_view(), name="low_products"),
    url(r'^products/new/$', inv_views.ProductCreateView.as_view(), name="create_product"),
    url(r'^appointments/$', inv_views.AllAppointmentsView.as_view(), name='all_appointments'),
    url(r'^appointments/new/$', inv_views.AppointmentCreateView.as_view(), name='add_appointment'),
    url(r'^services/$', inv_views.AllServicesView.as_view(), name='all_services'),
    url(r'^services/new/$', inv_views.ServiceCreateView.as_view(), name="create_service"),
    url(r'^appointments/delete/(?P<app_id>\d+)$', inv_views.AppointmentDelete.as_view(), name='delete_appointment'),
    url(r'^appointments/update/(?P<app_id>\d+)$', inv_views.AppointmentUpdate.as_view(), name='update_appointment'),
    url(r'^services/update/(?P<serv_id>\d+)$', inv_views.ServiceUpdate.as_view(), name='update_service'),
    url(r'^services/delete/(?P<serv_id>\d+)$', inv_views.ServiceDelete.as_view(), name='delete_service'),
]
