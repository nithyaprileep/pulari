from django import forms
from .models import *

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['feed', 'quantity', 'rate', 'total_amount']
        widgets = {
            'feed': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
        }



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'feed', 'quantity', 'rate', 'total_amount', 'paid_amount']
        widgets = {
            'feed': forms.Select(attrs={'class': 'form-select'}),
            'rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
        }
