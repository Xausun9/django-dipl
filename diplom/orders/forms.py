from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quanity']
        labels = {
            'quanity': 'Количество справок',
        }


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status", "comment"]
