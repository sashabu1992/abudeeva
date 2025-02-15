import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .specifications.blazers import BlazersAttributes
from .specifications.dresses import DressesAttributes
from .specifications.general import Color, Size
from django.shortcuts import render, get_object_or_404, redirect
from .models import CategoryShop, TovarShop
from django.db.models import Min, Max
from ..cart.models import Cart


logger = logging.getLogger(__name__)

def shop_index(request):
    return render(request, 'shop/shop.html')


def category_tovar(request, slug_category):
    # Получаем категорию по slug
    category = get_object_or_404(CategoryShop, slug=slug_category)

    # Получаем все товары из этой категории
    tovars = TovarShop.objects.filter(category=category, is_draft=True)

    # Получаем минимальную и максимальную цену для товаров в категории
    min_price = tovars.aggregate(min_price=Min('price'))['min_price'] or 0
    max_price = tovars.aggregate(max_price=Max('price'))['max_price'] or 10000

    # Получаем уникальные цвета и размеры для товаров в категории
    # Используем GenericRelation для фильтрации
    colors = Color.objects.filter(
        dressesattributes__tovar__in=tovars
    ).distinct()

    sizes = Size.objects.filter(
        dressesattributes__tovar__in=tovars
    ).distinct()

    # Формируем хлебные крошки
    breadcrumbs = list(category.get_ancestors(include_self=False))  # Исключаем текущую категорию


    # Передаем данные в шаблон
    context = {
        'category': category,
        'tovars': tovars,
        'breadcrumbs': breadcrumbs,
        'colors': colors,
        'sizes': sizes,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'shop/tovar_list.html', context)



def tovar_detail(request, slug_category, slug_tovar):

    # Получаем товар по slug и категории
    tovar = get_object_or_404(TovarShop, slug=slug_tovar, category__slug=slug_category)

    category = get_object_or_404(CategoryShop, slug=slug_category)

    # Получаем все товары из категории, исключая текущий товар
    tovars = TovarShop.objects.filter(category=category, is_draft=True).exclude(slug=slug_tovar)[:6]

    # Получаем фотографии товара
    photos = tovar.tovargallery_set.all()

    # Получаем категорию товара и всех её родителей
    category = tovar.category
    breadcrumbs = []
    while category:
        breadcrumbs.append(category)
        category = category.parent  # Переходим к родительской категории

    # Переворачиваем список, чтобы начать с корневой категории
    breadcrumbs = breadcrumbs[::-1]

    # Определяем модель характеристик в зависимости от категории
    attributes = None
    if tovar.category.attribute_type == 'dresses':
        attributes = DressesAttributes.objects.filter(content_type=ContentType.objects.get_for_model(tovar),
                                                     object_id=tovar.id).first()
    elif tovar.category.attribute_type == 'blazers':
        attributes = BlazersAttributes.objects.filter(content_type=ContentType.objects.get_for_model(tovar),
                                                     object_id=tovar.id).first()

    # Создаем словарь для характеристик
    properties = {}
    if attributes:
        # Динамически извлекаем все поля модели характеристик
        for field in attributes._meta.get_fields():
            # Исключаем служебные поля (GenericRel, ForeignKey и т.д.)
            if field.name not in ['id', 'content_type', 'object_id', 'content_object'] and not field.is_relation:
                field_value = getattr(attributes, field.name)
                if field_value:  # Добавляем только непустые значения
                    properties[field.verbose_name] = field_value

        # Добавляем цвета и размеры вручную, если они есть
        if hasattr(attributes, 'colors'):
            properties['Цвет'] = attributes.colors.all()
        if hasattr(attributes, 'sizes'):
            properties['Размер'] = attributes.sizes.all()

    # Передаем данные в контекст шаблона
    context = {
        'tovar': tovar,
        'tovars': tovars,
        'photos': photos,
        'breadcrumbs': breadcrumbs,
        'properties': properties,  # Передаем все характеристики
    }
    return render(request, 'shop/tovar_detail.html', context)

def filter_tovars(request):
    try:
        # Получаем параметры фильтров из запроса
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 10000)

        # Преобразуем в числа
        min_price = float(min_price) if min_price else 0
        max_price = float(max_price) if max_price else 10000

        selected_colors = request.GET.getlist('colors')  # Используем 'colors' без []
        selected_sizes = request.GET.getlist('sizes')    # Используем 'sizes' без []

        # Фильтруем товары по цене
        tovars = TovarShop.objects.filter(
            price__gte=min_price,
            price__lte=max_price,
        )

        # Фильтруем по цветам, если они выбраны
        if selected_colors:
            tovars = tovars.filter(
                dresses_attributes__colors__id__in=selected_colors
            ).distinct()

        # Фильтруем по размерам, если они выбраны
        if selected_sizes:
            tovars = tovars.filter(
                dresses_attributes__sizes__id__in=selected_sizes
            ).distinct()

        # Рендерим шаблон с отфильтрованными товарами
        return render(request, 'shop/chunk/tovar_list_filter.html', {'tovars': tovars})
    except Exception as e:
        # Логируем ошибку и возвращаем 500
        print(f"Ошибка: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)



@require_POST
def add_to_cart(request, tovar_id):
    try:
        # Получаем товар по ID
        tovar = get_object_or_404(TovarShop, id=tovar_id)

        # Собираем свойства из POST-запроса
        properties = {}
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken', 'quantity']:  # Исключаем служебные поля
                properties[key] = value

        # Добавляем товар в корзину
        cart = Cart(request)
        cart.add(tovar, properties=properties)


        # Возвращаем JSON-ответ
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_quantity(),
        })
    except TovarShop.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден',
        }, status=404)
    except Exception as e:
        logger.error(f"Error adding product to cart: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)

@require_POST
def remove_from_cart(request, key):
    try:
        cart = Cart(request)
        cart.remove(key)

        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_quantity(),  # Общее количество товаров
            'total_price': cart.get_total_price(),    # Общая стоимость
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)

@require_POST
def update_cart_quantity(request, key):
    try:
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)

        if quantity < 1:
            raise ValueError("Количество не может быть меньше 1")

        print(quantity)
        cart = Cart(request)
        cart.update_quantity(key, quantity)

        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_quantity(),  # Общее количество товаров
            'total_price': cart.get_total_price(),    # Общая стоимость
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)
