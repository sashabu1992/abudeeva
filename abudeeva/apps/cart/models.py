import logging

from django.conf import settings
from decimal import Decimal
import json
import hashlib
from ..shop.models import TovarShop
from ..shop.specifications.general import Color, Size

logger = logging.getLogger(__name__)
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Order(models.Model):
    # Статусы заказа
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    # Способы оплаты
    PAYMENT_METHOD_CHOICES = (
        ('sbp', 'Оплата через СБП'),
        ('card', 'Оплата картой онлайн'),
        ('doli', 'Оплата долями'),
        ('sert', 'Подарочный сертификат'),
    )

    # Способы доставки
    DELIVERY_METHOD_CHOICES = (
        ('courier', 'Курьерская доставка'),
        ('pickup', 'Пункт самовывоза'),
    )

    # Пользователь (может быть NULL, если заказ от неавторизованного пользователя)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )

    # Данные для неавторизованных пользователей
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')

    # Информация о заказе
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, verbose_name='Способ доставки')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка')


    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))

    def get_total_quantity(self):
        """
        Возвращает общее количество товаров в заказе.
        """
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    tovar = models.ForeignKey(TovarShop, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    properties = models.JSONField(default=dict, verbose_name='Свойства товара')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _generate_key(self, tovar_id, properties):
        """
        Генерирует уникальный ключ для товара на основе его ID и свойств.
        """
        properties_str = json.dumps(properties, sort_keys=True)
        key = f"{tovar_id}_{hashlib.md5(properties_str.encode()).hexdigest()}"
        return key

    def add(self, tovar, properties=None, quantity=1):
        """
        Добавляет товар в корзину.
        """
        properties = properties or {}
        key = self._generate_key(tovar.id, properties)

        if key not in self.cart:
            self.cart[key] = {
                'tovar_id': str(tovar.id),
                'quantity': 0,
                'price': str(tovar.price),
                'properties': properties,
            }
        self.cart[key]['quantity'] += quantity
        self.save()

    def update_quantity(self, key, quantity):

        if key in self.cart:
            self.cart[key]['quantity'] = quantity
            print(f"Обновлено количество товара {key}: {quantity}")  # Логируем изменение
            self.save()

    def save(self):
        self.session.modified = True


    def remove(self, key):
        """
        Удаляет товар из корзины по ключу.
        """
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        tovar_ids = [item['tovar_id'] for item in self.cart.values()]
        tovars = TovarShop.objects.filter(id__in=tovar_ids)
        cart = self.cart.copy()

        for tovar in tovars:
            for key, item_data in cart.items():
                if item_data['tovar_id'] == str(tovar.id):
                    item_data['tovar'] = tovar
                    item_data['price'] = Decimal(item_data['price'])
                    item_data['total_price'] = item_data['price'] * item_data['quantity']
                    yield key, item_data

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_items(self):
        """
        Возвращает список товаров в корзине с дополнительной информацией.
        """
        items = []
        for key, item_data in self.cart.items():
            if 'tovar_id' not in item_data:
                continue  # Пропускаем элементы с неправильной структурой

            try:
                tovar = TovarShop.objects.get(id=item_data['tovar_id'])
            except TovarShop.DoesNotExist:
                continue  # Пропускаем товары, которые больше не существуют

            properties = item_data.get('properties', {})

            # Преобразуем ID характеристик в читаемые значения
            readable_properties = {}
            for key_prop, value in properties.items():
                if key_prop == 'color' and value:
                    try:
                        color = Color.objects.get(id=value)
                        readable_properties['Цвет'] = color.name
                    except Color.DoesNotExist:
                        readable_properties['Цвет'] = 'Неизвестный цвет'
                elif key_prop == 'size' and value:
                    try:
                        size = Size.objects.get(id=value)
                        readable_properties['Размер'] = size.code
                    except Size.DoesNotExist:
                        readable_properties['Размер'] = 'Неизвестный размер'
                else:
                    readable_properties[key_prop] = value

            items.append({
                'key': key,  # Уникальный ключ товара
                'tovar': tovar,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'properties': readable_properties,  # Используем преобразованные свойства
            })
        return items

    def get_total_price(self):
        """
        Возвращает общую стоимость всех товаров в корзине.
        """
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_quantity(self):
        """
        Возвращает общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
