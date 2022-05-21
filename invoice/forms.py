from django import forms
from django.forms import formset_factory, widgets
from .models import Invoice1, Invoice2
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


CURRENCY=[('₹','Indian Rupee (INR)'),
          ('$','United States Dollar (USD)'),
          ('﷼','Qatar Riyal (QAR)'),
          ('£','Egypt Pound (EGP)'),
          ('¥','Japan Yen (JPY)'),
          ('د.إ','Emirati Dirham (AED)')]



FOOTER=[('https://svgshare.com/i/fkr.svg','Default')]

class InvoiceForm1(forms.Form):


    # service = forms.ChoiceField(
    #     label ='Select Service',
    #     choices=CHOICES,
    #     widget=forms.RadioSelect)

    currency = forms.ChoiceField(
        label='Select Currency',
        choices=CURRENCY,
        widget = forms.Select(attrs={
            'class': 'form-control',
        })
    )

    footer = forms.ChoiceField(
        label='Select Footer',
        choices=FOOTER,
        widget = forms.Select(attrs={
            'class': 'form-control',
        })
    )


    #fields = ['customer', 'message']
    customer = forms.CharField(max_length=50,
        label='Customer Name',
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Customer Name',
        'rows':1
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
        'type':'date'
        })

    )

    #billing_address = forms.CharField(
    #    label='Billing Address',
    #    widget=forms.TextInput(attrs={
    #        'class': 'form-control',
    #        'placeholder': '',
    #        'rows':1
    #    })
    #)

    # service_message = forms.CharField(max_length=34,
    #     label='Service Description',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Service Description',
    #         'rows':1
    #     })
    # )

    fulldescriptionrigs = forms.CharField(
        label='Additional Notes',
        initial= f'Apro Rigs.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows':2
        })
    )
    fulldescriptionit = forms.CharField(
        label='Additional Notes',
        initial=f'Apro IT Solutions.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )
    fulldescriptioncms = forms.CharField(
        label='Additional Notes',
        initial=f'Apro CMS.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )
    fulldescriptionaprohosting = forms.CharField(
        label='Additional Notes',
        initial=f'Apro Hosting.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )


    service_type = forms.CharField(max_length=48,
        label='Service Message',
        initial=f'Apro Rigs - Mining Rigs',
        widget=forms.TextInput(attrs={
            'class': 'form-control',

            'rows':1
        })
    )
    termsandconditionsaprorigs = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro Rigs\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )

    termsandconditionsaproitsolutions = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro IT Solutions\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )
    termsandconditionsaprocms = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro CMS\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )

    termsandconditionsaprohosting = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro Hosting\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )

class InvoiceForm2(forms.Form):


    #service = forms.ChoiceField(
    #  label = 'Select Service',
    #  choices = CHOICES,
    #  widget = forms.RadioSelect)

    currency = forms.ChoiceField(
        label='Select Currency',
        choices=CURRENCY,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    footer = forms.ChoiceField(
        label='Select Footer',
        choices=FOOTER,
        widget = forms.Select(attrs={
            'class': 'form-control',
        })
    )


    #fields = ['customer', 'message']
    customer = forms.CharField(max_length=50,
        label='Customer Name',
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Customer Name',
        'rows':1
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
        'type':'date'
        })

    )
    bill_title = forms.CharField(max_length=148,
        label='Estimate Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bill Description',
            'rows':1
        })
    )
    #billing_address = forms.CharField(
    #    label='Billing Address',
    #    widget=forms.TextInput(attrs={
    #        'class': 'form-control',
    #        'placeholder': '',
    #        'rows':1
    #    })
    #)

    # service_message = forms.CharField(max_length=34,
    #     label='Service Description',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Service Description',
    #         'rows':1
    #     })
    # )

    fulldescriptionrigs = forms.CharField(
        label='Additional Notes',
        initial= f'Apro Rigs.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows':2
        })
    )
    fulldescriptionit = forms.CharField(
        label='Additional Notes',
        initial=f'Apro IT Solutions.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )
    fulldescriptioncms = forms.CharField(
        label='Additional Notes',
        initial=f'Apro CMS.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )
    fulldescriptionaprohosting = forms.CharField(
        label='Additional Notes',
        initial=f'Apro Hosting.\n* HiveOS is free for 1 rig, additional rigs $3 per month.\n* Brand Warranty does not cover riser cables, splitter cables and pcie hubs. \n* GST 18% applicapble on the final invoice depending on the client profile',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Additional Notes',
            'rows': 2
        })
    )


    service_type = forms.CharField(max_length=48,
        label='Service Message',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apro Rigs - Mining Rigs',
            'rows':1
        })
    )
    termsandconditionsaprorigs = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro Rigs\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )

    termsandconditionsaproitsolutions = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro IT Solutions\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )
    termsandconditionsaprocms = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro CMS\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )

    termsandconditionsaprohosting = forms.CharField(
        label='Terms and Conditions',
        initial= f'• Apro Hosting\n• Requires a 100% down payment upon the start of the build. \n• Estimate Validity - 7 days. ',
        widget=forms.Textarea(attrs={
             'class': 'form-control',
             'placeholder': 'Enter Terms and Conditions',
             'rows':2
         })
     )


class LineItemForm1(forms.Form):
    
    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Product/Service Name'
        })
    )
    description = forms.CharField(min_length=40,
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Product Description',
            "rows":1
        })
    )
    quantity = forms.IntegerField(min_value=1,
        label='Qty',
        widget=forms.NumberInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'


        }) #quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate',
        widget=forms.NumberInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'

        })
    )
    #amount = forms.DecimalField(
       #disabled = False,
      #label='Amount $',
       #widget=forms.TextInput(attrs={
        #    'class': 'form-control input',
        #})
    #)
class LineItemForm2(forms.Form):

    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Product/Service Name'
        })
    )
    description = forms.CharField(min_length=5,
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Product Description',
            "rows":1
        })
    )
    quantity = forms.IntegerField(min_value=1,
        label='Qty',
        widget=forms.NumberInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'


        }) #quantity should not be less than one
    )

    # rate = forms.DecimalField(
    #     label='Rate',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'form-control input rate',
    #         'placeholder': 'Rate'
    #
    #     })
    # )
    amount = forms.CharField(
       disabled = False,
       label='Amount $',
       widget=forms.TextInput(attrs={
           'class': 'form-control input',
        })
    )


LineItemFormset1 = formset_factory(LineItemForm1, extra=1)
LineItemFormset2 = formset_factory(LineItemForm2, extra=1)










