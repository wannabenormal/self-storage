from users import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from storages.views import view_storages


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('boxes/', view_storages, name='boxes'),
    path('account/', views.lk, name='account'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('pay/', TemplateView.as_view(template_name='pay.html'), name='pay'),
    path('users/', include('users.urls')),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('manager/', include('storages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
