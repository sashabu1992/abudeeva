from django import forms

from apps.cart.models import Order

class GuestOrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(max_length=250, label='Адрес')
    postal_code = forms.CharField(max_length=20, label='Почтовый индекс')
    city = forms.CharField(max_length=100, label='Город')
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, label='Способ оплаты')
    delivery_method = forms.ChoiceField(choices=Order.DELIVERY_METHOD_CHOICES, label='Способ доставки')