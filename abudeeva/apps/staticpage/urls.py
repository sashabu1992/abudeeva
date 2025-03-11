
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PokupatelPage, name='pokupatel'),
    path('<slug:slug_stpage>/', views.StaticPageDetail, name='slug_stpage'),
]