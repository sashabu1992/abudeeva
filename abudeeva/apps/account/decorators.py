from django.contrib import messages
from django.shortcuts import redirect


def anonymous_required(view_func):
    """
    Декоратор для проверки, что пользователь не авторизован.
    Если пользователь авторизован, он будет перенаправлен на главную страницу.
    """
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы уже авторизованы.')
            return redirect('lk')  # Перенаправляем на личный кабинет или другую страницу
        return view_func(request, *args, **kwargs)
    return wrapped_view