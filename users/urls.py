from django.urls import path, include
from users import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
]
