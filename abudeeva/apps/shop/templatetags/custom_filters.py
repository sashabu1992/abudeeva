from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from ..models import CategoryShop  # Импортируем вашу модель

register = template.Library()

@register.simple_tag
def render_categories():
    """
    Формирует HTML-структуру для категорий без вложенных ul.
    """
    def build_tree(category):
        # Формируем данные для текущей категории
        subcategories = category.get_children()
        subnav = {}

        # Собираем подкатегории для data-subnav
        for subcategory in subcategories:
            subnav[subcategory.h1] = reverse('category_tovar', kwargs={'slug_category': subcategory.slug})

        # Формируем HTML для текущей категории
        html = f'<li class="category-item"><a data-subnav="{subnav}" href="{reverse("category_tovar", kwargs={"slug_category": category.slug})}">{category.h1}</a></li>'
        return html

    # Получаем корневые категории (те, у которых нет родителя)
    categories = CategoryShop.objects.filter(parent=None)

    # Начинаем формирование HTML с корневых категорий
    html = '<ul class="category-list">'
    for category in categories:
        html += build_tree(category)
    html += '</ul>'

    return mark_safe(html)


@register.filter
def format_price(value):
    """
    Форматирует цену: добавляет пробелы между тысячами и убирает .00, если они есть.
    """
    if value is None:
        return ""

    # Преобразуем Decimal или float в строку с двумя знаками после запятой
    price_str = f"{value:,.2f}"

    # Убираем .00, если они есть
   #if price_str.endswith(".00"):
   #    price_str = price_str[:-3]

    # Заменяем запятые на пробелы (для разделения тысяч)
    price_str = price_str.replace(",", " ")

    return price_str

@register.filter
def pluralize_products(count):
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} товар"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return f"{count} товара"
    else:
        return f"{count} товаров"