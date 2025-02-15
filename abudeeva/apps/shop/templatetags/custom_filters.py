from django import template

register = template.Library()


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