from django.shortcuts import render, get_object_or_404

from apps.shop.models import CategoryShop, TovarShop


def index(request):
    tovars_popular = TovarShop.objects.filter(is_draft=True, is_popular=True)
    tovars_new = TovarShop.objects.filter(is_draft=True, is_new=True)
    tovars_category = CategoryShop.objects.filter(is_draft=True)
    # Передаем данные в шаблон
    context = {
        'tovars_popular':tovars_popular,
        'tovars_new':tovars_new,
        'tovars_category':tovars_category
    }
    return render(request, 'pages/index.html', context)


