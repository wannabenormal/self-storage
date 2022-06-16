from django.urls import path
from django.shortcuts import redirect

from . import views


urlpatterns = [
    path('orders/', views.view_orders, name="view_orders"),
]