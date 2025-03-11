
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogPage, name='BlogPage'),
    path('<slug:slug_blogpage>/', views.BlogPageDetail, name='BlogPageDetail'),
]