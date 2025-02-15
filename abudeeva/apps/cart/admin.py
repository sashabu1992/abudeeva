# admin.py
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):  # или admin.StackedInline для другого стиля
    model = OrderItem
    extra = 0  # Не показывать пустые поля для добавления новых товаров
    readonly_fields = ('tovar', 'price', 'quantity', 'properties')  # Поля только для чтения
    can_delete = False  # Запретить удаление товаров через админку

    def has_add_permission(self, request, obj=None):
        return False  # Запретить добавление новых товаров через админку




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name',  'colored_status', 'payment_method', 'delivery_method',
        'get_total_cost', 'created', 'paid'
    )
    list_filter = (
        'status', 'payment_method', 'delivery_method', 'paid', 'created'
    )
    search_fields = (
        'id', 'user__username', 'first_name', 'last_name', 'email', 'phone'
    )
    readonly_fields = ('created', 'updated', 'get_total_cost')
    inlines = [OrderItemInline]
    list_per_page = 20
    date_hierarchy = 'created'
    actions = ['mark_as_paid', 'mark_as_shipped']

    fieldsets = (
        ('Информация о заказе', {
            'fields': (
                'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'status',
                'payment_method', 'delivery_method', 'discount', 'paid'
            )
        }),
        ('Даты', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Общая стоимость'

    def colored_status(self, obj):
        # Определяем цвет для каждого статуса
        colors = {
            'pending': 'orange',  # Оранжевый для "Ожидает обработки"
            'processing': 'blue',  # Синий для "В обработке"
            'shipped': 'green',  # Зеленый для "Отправлен"
            'delivered': 'purple',  # Фиолетовый для "Доставлен"
            'cancelled': 'red',  # Красный для "Отменен"
        }
        # Возвращаем статус с цветным оформлением
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),  # По умолчанию черный цвет, если статус не найден
            obj.get_status_display()  # Отображаемое значение статуса
        )
    colored_status.short_description = 'Статус'  # Название колонки
    colored_status.admin_order_field = 'status'  # Позволяет сортировать по статусу
    colored_status.allow_tags = True  # Разрешаем использование HTML-тегов