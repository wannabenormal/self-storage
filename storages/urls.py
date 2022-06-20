from django.urls import path

from . import views

app_name = 'storages'

urlpatterns = [
    path('', views.view_manager_menu, name='manager_menu'),
    path('expired_orders/', views.view_expired_orders, name='expired_orders'),
    path('orders/', views.view_orders, name='view_orders'),
]
