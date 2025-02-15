from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Cart, OrderItem, Order  # Импортируем класс Cart
from django.shortcuts import render, redirect
from .forms import GuestOrderForm

def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.get_items()

    # Если пользователь авторизован, предзаполняем форму данными из профиля
    if request.user.is_authenticated:
        profile = request.user.profile
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': profile.phone,
            'address': profile.address,
            'postal_code': profile.postal_code,
            'city': profile.city,
        }
        form = GuestOrderForm(initial=initial_data)
    else:
        form = GuestOrderForm()

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'form': form,
    }
    return render(request, 'shop/cart_detail.html', context)


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Получаем профиль пользователя
            profile = request.user.profile
            # Создание заказа для авторизованного пользователя
            order = Order.objects.create(
                user=request.user,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                phone=profile.phone,  # Используем поле из профиля
                address=profile.address,
                postal_code=profile.postal_code,
                city=profile.city,
                payment_method=request.POST.get('payment_method'),
                delivery_method=request.POST.get('delivery_method'),
                discount=10
            )
        else:
            # Создание заказа для неавторизованного пользователя
            form = GuestOrderForm(request.POST)
            if form.is_valid():
                order = Order.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    postal_code=form.cleaned_data['postal_code'],
                    city=form.cleaned_data['city'],
                    payment_method=form.cleaned_data['payment_method'],
                    delivery_method=form.cleaned_data['delivery_method'],
                    discount=10
                )
            else:
                # Если форма невалидна, возвращаем ошибки
                return JsonResponse({'success': False, 'errors': form.errors})

        # Добавление товаров в заказ
        for item in cart.get_items():
            OrderItem.objects.create(
                order=order,
                tovar=item['tovar'],
                price=item['price'],
                quantity=item['quantity'],
                properties=item['properties']
            )

        # Очистка корзины
        cart.clear()

        # Перенаправление на страницу благодарности
        return JsonResponse({'success': True, 'redirect_url': f'/lk/order/{order.id}/'})

    return JsonResponse({'success': False, 'message': 'Некорректный запрос'})

