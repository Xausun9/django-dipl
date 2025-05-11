from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'group', 'quanity']

class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'comment']
