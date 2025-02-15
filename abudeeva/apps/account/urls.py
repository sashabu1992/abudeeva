from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lk, name='lk'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('password-change/', views.password_change, name='password_change'),  # Изменение пароля авторизованых
    path('order/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_id, name='order_id'),
    path('wishlist/', views.wishlist_list, name='wishlist_list'),
    path('loyalty-card/', views.loyalty_card, name='loyalty_card'),


    # Восстановление пароля с использованием ваших шаблонов
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]