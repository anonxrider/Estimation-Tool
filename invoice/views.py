# FROM SECTION
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from .models import LineItem1, Invoice1, LineItem2, Invoice2
from .forms import LineItemFormset1, InvoiceForm1, LineItemFormset2, InvoiceForm2
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout

# IMPORT SECTION
import pdfkit
import csv
import bleach
import datetime
import logging

# LOGGING CONFIGURATION
logging.basicConfig(filename="warnings.log", encoding="utf-8", level=logging.WARNING)

ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

# LOGOUT SECTION AND REDIRECT REQUEST
# ADMIN LOGIN LINK /ADMIN/LOGIN/?NEXT=/ADMIN/
def logout(request):
    logging.warning("Logout Requested")
    auth_logout(request)
    logging.warning("Successfully Logged Out and Redirect to Admin Login")
    return redirect("/admin/login/?next=/admin/")

# INVOICE TYPE 2 NO TAX CUSTOMERS
class InvoiceListView2(View):
    def get(self, *args, **kwargs):
        invoices2 = Invoice2.objects.all().order_by("-id")
        context = {
            "invoices2": invoices2,
        }
        return render(self.request, "invoice/invoice-list-2.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice2_ids = request.POST.getlist("invoice2_id")
        invoice2_ids = list(map(int, invoice2_ids))
        invoices2 = Invoice2.objects.filter(id__in=invoice2_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-2")


# INVOICE TYPE 1 TAX (GST) CUSTOMERS
# INVOICE LIST TYPE 1 VIEW MAIN WITH LOGIN ALSO CHECKED
class InvoiceListView1(LoginRequiredMixin, View):
    # LOGIN URL /ADMIN/LOGIN/?NEXT=/ADMIN/
    login_url = "/admin/login/?next=/admin/"

    def get(self, *args, **kwargs):
        # POPULATE DATA IN DATABASE TO INVOICE-LIST.HTML PAGE WITH ORDER_BY ID
        # SORT BY LATEST ID OR UPDATED ID
        invoices1 = Invoice1.objects.all().order_by("-id")
        total_count = Invoice1.objects.count()
        logging.warning("Invoice Ordered by -id from Database")
        context = {
            "invoices1": invoices1,
            "total_count": total_count,
            "main_title": "APRO ESTIMATE",
            "css_link_a": "https://fonts.googleapis.com/icon?family=Material+Icons",
            "css_link_b": "static\css\style.css",
            "css_link_c": "https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css",
            "css_link_d": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            "image_src_a": "https://media-exp1.licdn.com/dms/image/C4D03AQEw4CeRYGE1Fg/profile-displayphoto-shrink_200_200/0/1602676941276?e=1655337600&v=beta&t=SYbeRRL8MilPLKuOpl5EG1U6nBtAtw5pLb3G_sQXqo4",
            "title_a": "Dashboard",
            "title_b": "Create Estimate",
            "title_c": "View Estimate",
            "title_d": "Filter by Date (+)",
            "title_e": "Filter by Date (-)",
            "title_f": "Admin Panel",
            "title_g": "Export As CSV",
            "title_h": "Export As PDF",
            "title_i": "Create New Tax Based Estimate",
            "title_j": "More Info",
            "title_k": "View Tax Estimates",
            "title_l": "Logout",
            "title_m": "Search",
            "table_head_a": "CUSTOMER ID",
            "table_head_b": "DATE",
            "table_head_c": "CUSTOMER NAME",
            "table_head_d": "SERVICE TYPE",
            "table_head_e": "GST(%)",
            "table_head_f": "TOTAL",
            "table_head_excluded_GST": "(excluded GST)",
            "table_head_included_GST": "(included GST)",
            "table_head_view": "View",
            "table_head_edit": "Edit",
            "table_head_delete": "Delete",
            "table_head_download": "Download",
        }
        # RENDER AND SHOW OUTPUT TO INVOICE-LIST.HTML
        logging.warning("Invoice Lists Generated Successfully Ordered by -id")

        return render(self.request, "invoice/invoice-list.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list")


class InvoiceListView1datenegative(LoginRequiredMixin, View):
    logging.warning("Filtered by -Date")
    login_url = "/admin/login/?next=/admin/"

    def get(self, *args, **kwargs):
        invoices1 = Invoice1.objects.all().order_by("-date")
        logging.warning("Invoice Ordered by -date from Database")
        context = {
            "invoices1": invoices1,
        }
        logging.warning("Invoice Lists Generated Successfully Ordered by -date")
        return render(self.request, "invoice/invoice-list-date-negative.html", context)

    def post(self, request):

        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice2_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-date-negative")


class InvoiceListView1datepositive(LoginRequiredMixin, View):
    login_url = "/admin/login/?next=/admin/"

    def get(self, *args, **kwargs):
        logging.warning("Filtered by +Date")
        invoices1 = Invoice1.objects.all().order_by("date")
        context = {
            "invoices1": invoices1,
        }
        return render(self.request, "invoice/invoice-list-date-positive.html", context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice1_ids = request.POST.getlist("invoice1_id")
        invoice1_ids = list(map(int, invoice1_ids))
        invoices1 = Invoice1.objects.filter(id__in=invoice1_ids)
        # import pdb;pdb.set_trace()
        return redirect("invoice:invoice-list-date-positive")


@login_required(login_url="/admin/login/?next=/admin/")
def createInvoice1(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset1(request.GET or None)
        form = InvoiceForm1(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset1(request.POST)
        form = InvoiceForm1(request.POST)
        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        if servicea == "http://apropack.com/assets/apro-rigs.svg":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]
        elif servicea == "http://apropack.com/assets/apro-it.svg":
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]
        elif servicea == "http://apropack.com/assets/apro-hosting.svg":
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]
        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]
        defaultval1 = "This estimate specifies the price for"
        defaultval2 = "for your company."
        customernamecleandata = bleach.clean(
            form.data["customer"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        billtitlefrontcleandata = defaultval1
        billtitlebackcleandata = defaultval2
        gstcleandata = bleach.clean(
            gstpercentageinfloat,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        termsandconditioncleandata = bleach.clean(
            terms1,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        additionalnotescleandata = bleach.clean(
            additionalnotes,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        datecleandata = bleach.clean(
            form.data["date"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicetypecleandata = bleach.clean(
            form.data["service_type"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        servicecleandata = bleach.clean(
            servicea,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        currencycleandata = bleach.clean(
            currencycountry,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        footercleandata = bleach.clean(
            footerdefault,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=False,
            strip_comments=True,
        )
        Str1 = billtitlefrontcleandata
        Str2 = servicetypecleandata
        Str3 = billtitlebackcleandata
        abcs = Str1 + " " + Str2 + "" + Str3
        print(abcs)
        if form.is_valid():
            invoice1 = Invoice1.objects.create(
                customer=customernamecleandata,
                bill_titlefront=billtitlefrontcleandata,
                bill_titleback=billtitlebackcleandata,
                gst=gstcleandata,
                termsandconditions=termsandconditioncleandata,
                fulldescription=additionalnotescleandata,
                bill_title=abcs,
                date=datecleandata,
                service_type=servicetypecleandata,
                gstpercentage=b,
                service=servicecleandata,
                currency=currencycleandata,
                footer=footercleandata,
            )
            # invoice.save()
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    servicecleandata = bleach.clean(
                        service,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )
                    descriptioncleandata = bleach.clean(
                        description,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES,
                        strip=False,
                        strip_comments=True,
                    )

                    LineItem1(
                        customer=invoice1,
                        service=servicecleandata,
                        description=descriptioncleandata,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice1.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)
            invoice1.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice1.subtotal = abc
            invoice1.save()

            try:
                generate_PDF1(request, id=invoice1.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }

    return render(request, "invoice/invoice-create.html", context)


def createInvoice2(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = "Apro IT Solutions"
    if request.method == "GET":
        formset = LineItemFormset2(request.GET or None)
        form = InvoiceForm2(request.GET or None)
    elif request.method == "POST":
        formset = LineItemFormset2(request.POST)
        form = InvoiceForm2(request.POST)

        gstpercentageinfloat = form.data["gst"]
        a = float(gstpercentageinfloat) * 100
        b = int(a)
        servicea = form.data["service"]
        if servicea == "https://www.aprorigs.com/wp-content/uploads/2021/11/logo3.png":
            terms1 = form.data["termsandconditionsaprorigs"]
            additionalnotes = form.data["fulldescriptionrigs"]

        elif (
            servicea
            == "https://aproitsolutions.com/wp-content/uploads/2019/07/apro-logo-for-web-new-dark-1.png"
        ):
            terms1 = form.data["termsandconditionsaproitsolutions"]
            additionalnotes = form.data["fulldescriptionit"]

        elif (
            servicea == "https://aprohosting.com/wp-content/uploads/2021/11/logo-02.png"
        ):
            terms1 = form.data["termsandconditionsaprohosting"]
            additionalnotes = form.data["fulldescriptionaprohosting"]

        else:
            terms1 = form.data["termsandconditionsaprocms"]
            additionalnotes = form.data["fulldescriptioncms"]

        currencycountry = form.data["currency"]
        footerdefault = form.data["footer"]

        if form.is_valid():
            invoice2 = Invoice2.objects.create(
                customer=form.data["customer"],
                bill_title=form.data["bill_title"],
                gst=gstpercentageinfloat,
                termsandconditions=terms1,
                fulldescription=additionalnotes,
                date=form.data["date"],
                service_type=form.data["service_type"],
                gstpercentage=b,
                service=servicea,
                currency=currencycountry,
                footer=footerdefault,
            )

            # invoice.save()

        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0

            for form in formset:
                service = form.cleaned_data.get("service")
                description = form.cleaned_data.get("description")
                quantity = form.cleaned_data.get("quantity")
                rate = form.cleaned_data.get("rate")

                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)

                    total += amount
                    LineItem2(
                        customer=invoice2,
                        service=service,
                        description=description,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                    ).save()
            invoice2.total_amount = total
            totala = float(total)
            gsta = float(gstpercentageinfloat)
            gsttotala = totala * gsta
            floata = gsttotala
            format_float = "{:.2f}".format(floata)

            invoice2.gsttotal = format_float
            subtotal = gsttotala + totala
            abc = float(subtotal)
            invoice2.subtotal = abc
            invoice2.save()

            try:
                generate_PDF2(request, id=invoice2.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect("/")
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, "invoice/invoice-create-2.html", context)


def view_PDF1(request, id=None):
    invoice1 = get_object_or_404(Invoice1, id=id)
    lineitem1 = invoice1.lineitem1_set.all()
    context = {
        "company": {
            "name": "APRO IT Solutions Pvt. Ltd.",
            "address001": "2nd Floor, Supriya Building, South Junction",
            "address002": "Chalakudy, Kerala - 680307, Tel. +91 62 386 83 058",
            # "phone": "+91 9746344984",
            "website": "www.aproitsolutions.com",
            "email": "info@aproitsolutions.com",
        },
        "invoice_id": invoice1.id,
        "invoice_gst": invoice1.gst,
        "invoice_total": invoice1.total_amount,
        "customer": invoice1.customer,
        "bill_title": invoice1.bill_title,
        "fulldescription": invoice1.fulldescription,
        "termsandconditions": invoice1.termsandconditions,
        "service": invoice1.service,
        "date": invoice1.date,
        "service_type": invoice1.service_type,
        "gstpercentage": invoice1.gstpercentage,
        "subtotal": invoice1.subtotal,
        "gsttotal": invoice1.gsttotal,
        "currency": invoice1.currency,
        "lineitem1": lineitem1,
    }
    return render(request, "invoice/pdf2oldnew.html", context)


def view_PDF2(request, id=None):
    invoice2 = get_object_or_404(Invoice2, id=id)
    lineitem2 = invoice2.lineitem2_set.all()

    context = {
        "company": {
            "name": "APRO IT Solutions Pvt. Ltd.",
            "address001": "2nd Floor, Supriya Building, South Junction",
            "address002": "Chalakudy, Kerala - 680307, Tel. +91 62 386 83 058",
            # "phone": "+91 9746344984",
            "website": "www.aproitsolutions.com",
            "email": "info@aproitsolutions.com",
        },
        "invoice_id": invoice2.id,
        "invoice_total": invoice2.total_amount,
        "customer": invoice2.customer,
        "bill_title": invoice2.bill_title,
        "fulldescription": invoice2.fulldescription,
        "termsandconditions": invoice2.termsandconditions,
        "service": invoice2.service,
        "date": invoice2.date,
        "service_type": invoice2.service_type,
        "subtotal": invoice2.subtotal,
        "currency": invoice2.currency,
        "lineitem2": lineitem2,
    }
    return render(request, "invoice/pdfout.html", context)


def generate_PDF1(request, id):
    options = {
        "page-size": "A4",
        "margin-top": "0.00in",
        "margin-right": "0.00in",
        "margin-bottom": "0.00in",
        "margin-left": "0.00in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }

    pdf = pdfkit.from_url(
        request.build_absolute_uri(reverse("invoice:invoice-detail", args=[id])),
        False,
        options=options,
    )
    response = HttpResponse(pdf, content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="pdf.pdf"'
    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


# PDF GENERATE SECTION FOR NON TAX CUSTOMERS
def generate_PDF2(request, id):
    options = {
        "page-size": "B4",
        "margin-top": "0.00in",
        "margin-right": "0.00in",
        "margin-bottom": "0.00in",
        "margin-left": "0.00in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(
        request.build_absolute_uri(reverse("invoice:invoice-detail", args=[id])),
        False,
        options=options,
    )
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="pdf.pdf"'
    return response


def change_status1(request):
    return redirect("invoice:invoice-list")


def view_4041(request, *args, **kwargs):
    return redirect("invoice:invoice-list")


# DELETE INVOICE SECTION FOR NON TAX CUSTOMERS
def deleteInvoice2(request, id):
    try:
        record = Invoice2.objects.get(id=id)
        record.delete()
    except:
        messages.info(request, f"The requested id doesnot exists!")
    return redirect("invoice:invoice-list-2")


# DELETE INVOICE SECTION FOR TAX CUSTOMERS
def deleteInvoice1(request, id):
    try:
        record = Invoice1.objects.get(id=id)
        record.delete()
    except:
        messages.info(request, f"The requested id doesnot exists!")
    return redirect("invoice:invoice-list")


# UPDATE RECORD SECTION A
def update1(request, id):
    invoice1 = Invoice1.objects.get(id=id)
    template = loader.get_template("invoice/edittaxcustomers.html")
    context = {
        "invoice1": invoice1,
    }
    return HttpResponse(template.render(context, request))


# UPDATE RECORD SECTION B
def updaterecord1(request, id):
    # CUSTOMER NAME
    customer = request.POST["customername"]
    # BILL TITLE
    bill_title = request.POST["billtitle"]
    # SERVICE TYPE
    service_type = request.POST["service_type"]
    invoice1 = Invoice1.objects.get(id=id)
    invoice1.customer = customer
    invoice1.bill_title = bill_title
    invoice1.service_type = service_type
    invoice1.save()
    messages.info(request, f"The Customer {customer} has been updated successfully!")
    return redirect("/")


# EXPORT SECTION CODE (DATABASE EXPORT TO CSV FILE)
def export(request):
    # EXPORT SECTION CONTENT TYPE TEXT/CSV
    logging.warning("User Requested CSV")
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    # DATAS TABLE COLUMN NAMES AND EXCEL COLUMN NAMES
    writer.writerow(
        ["id", "customer", "date", "service_type", "bill_title", "total_amount"]
    )
    for customers in Invoice1.objects.all().values_list(
        "id", "customer", "date", "service_type", "bill_title", "total_amount"
    ):
        writer.writerow(customers)
    logging.warning("CSV Written to File from Database")
    # ATTACHMENT FILE NAME CUSTOMERS.CSV
    response["Content-Disposition"] = 'attachment; filename="Customers.csv"'
    logging.warning("CSV Generated Successfully")
    return response
