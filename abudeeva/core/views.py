from django.shortcuts import render, get_object_or_404

from apps.shop.models import CategoryShop


def index(request):
    # Получаем категорию по slug
    category = CategoryShop.objects.all()
    # Передаем данные в шаблон
    context = {
        'category': category,
    }
    return render(request, 'pages/index.html', context)


