from users import views as userviews
from storages import views as storagesviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from storages.views import view_storages


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', storagesviews.view_index, name='index'),
    path('api/', include('api.urls')),
    path('account/', userviews.lk, name='account'),
    path('boxes/', view_storages, name='boxes'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('pay/', TemplateView.as_view(template_name='pay.html'), name='pay'),
    path('users/', include('users.urls')),
    path('register/', userviews.register, name='register'),
    path('signin/', userviews.signin, name='signin'),
    path('manager/', include('storages.urls')),
    path('order_details/<product_number>/', storagesviews.order_details, name='order_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
