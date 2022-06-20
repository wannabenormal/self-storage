from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('save_order', views.save_order, name='save_order'),
    path('open_box', views.open_box, name='open_box'),
]
