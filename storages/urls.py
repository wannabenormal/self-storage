from django.urls import path
from django.shortcuts import redirect

from . import views


urlpatterns = [
    path('expired_orders', views.view_expired_orders, name='expired_orders'),
    path('orders/', views.view_orders, name='view_orders'),
]