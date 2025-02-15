from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .decorators import anonymous_required  # Импортируем декоратор
from .models import Profile
from ..cart.models import Order, OrderItem


@login_required
def lk(request):
    user = request.user
    profile = user.profile

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'account/lk.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    # Создаем список уникальных товаров для каждого заказа
    for order in orders:
        unique_items = {item.tovar.id: item for item in order.items.all()}.values()
        order.unique_items = unique_items  # Добавляем уникальные товары к заказу

    context = {'orders': orders}
    return render(request, 'account/order_list.html', context)

@login_required
def wishlist_list(request):
    context = {}
    return render(request, 'account/wishlist_list.html', context)

@login_required
def loyalty_card(request):
    context = {}
    return render(request, 'account/loyalty_card.html', context)

@anonymous_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})

@anonymous_required
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', 'lk')  # Перенаправление после входа
                return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    return render(request, 'account/login.html', {'form': form, 'next': request.GET.get('next', '')})


def user_logout(request):
    logout(request)
    return redirect('index')



@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # Создаем профиль, если его нет

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'account/profile.html', context)

@login_required
def profile_edit(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # Создаем профиль, если его нет

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'account/profile_edit.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Обновляем сессию, чтобы пользователь не вышел
            messages.success(request, 'Ваш пароль успешно изменен!')
            return redirect('lk')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/password_change.html', {'form': form})


def order_id(request, order_id):
    # Получаем заказ или возвращаем 404, если заказ не существует или не принадлежит пользователю
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'account/order_id_view.html', {'order': order})