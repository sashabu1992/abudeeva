# apps/shop/urls.py
from django.urls import path
from . import views  # Импортируем views из текущего приложения



urlpatterns = [
    path('', views.shop_index, name='shop_index'),  # Маршрут для главной страницы shop
    path('filter-tovars/', views.filter_tovars, name='filter_tovars'),
    path('add_to_cart/<int:tovar_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<str:key>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('<slug:slug_category>/', views.category_tovar, name='category_tovar'),
    path('<slug:slug_category>/<slug:slug_tovar>/', views.tovar_detail, name='tovar_detail'),

]