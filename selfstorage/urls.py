from users import views as userviews
from storages import views as storagesviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('boxes/', TemplateView.as_view(template_name='boxes.html'), name='boxes'),
    path('account/', views.lk, name='account'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('pay/', TemplateView.as_view(template_name='pay.html'), name='pay'),
    path('users/', include('users.urls')),
    path('register/', userviews.register, name='register'),
    path('signin/', userviews.signin, name='signin'),
    path('manager/', include('storages.urls')),
    path('order_details/<int:productid>', storagesviews.order_details, name='order_details'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
