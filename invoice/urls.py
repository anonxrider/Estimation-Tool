from django.contrib import admin
from django.urls import path
from .views import InvoiceListView1, createInvoice1, generate_PDF1, view_PDF1,update1,updaterecord1,deleteInvoice1, InvoiceListView1datenegative , InvoiceListView1datepositive
from .views import InvoiceListView2, createInvoice2, generate_PDF2, view_PDF2,deleteInvoice2, logout
from django.conf.urls import include
from .views import export
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404

app_name = 'invoice'
urlpatterns = [
    path('', InvoiceListView1.as_view(), name="invoice-list"),
    path('invoicefilterdatenegative', InvoiceListView1datenegative.as_view(), name="invoice-list-date-negative"),
    path('invoicefilterdatepositive', InvoiceListView1datepositive.as_view(), name="invoice-list-date-positive"),
    path('invoicelist', InvoiceListView2.as_view(), name="invoice-list-2"),


    path('create/', createInvoice1, name="invoice-create"),
    path('createnotax/', createInvoice2, name="invoice-create-2"),


    path('invoice-detail/<id>', view_PDF1, name='invoice-detail'),
    path('invoice-detail-notax/<id>', view_PDF2, name='invoice-detail-2'),



    path('invoice-download/<id>', generate_PDF1, name='invoice-download'),
    path('invoice-download-notax/<id>', generate_PDF2, name='invoice-download-2'),

    path('invoice-delete/<id>', deleteInvoice1, name='invoice-delete'),
    path('invoice-delete-notax/<id>', deleteInvoice2, name='invoice-delete-2'),

    path('update/<int:id>', update1, name='update'),


    path('update/updaterecord/<int:id>', updaterecord1, name='updaterecord'),

  path('export/', export, name='export'),

      path('logout/', logout, name='logout'),

]

