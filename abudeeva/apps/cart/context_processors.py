# cart/context_processors.py
from .models import Cart  # Импортируем ваш класс Cart

def cart_context(request):
    """
    Контекстный процессор для добавления корзины в контекст всех шаблонов.
    """
    cart = Cart(request)  # Создаем объект корзины на основе сессии
    return {
        'cart': cart,  # Добавляем корзину в контекст
    }