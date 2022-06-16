from django.contrib import admin
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import Order, Box, Storage


class BoxInline(admin.TabularInline):
    model = Box
    readonly_fields = ('number',)
    fields = (
        'storage',
        'number',
        'rental_price',
    )
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('renter',)

    inlines = [
        BoxInline,
    ]

    def response_post_save_change(self, request, obj):
        '''
        Возвращаем на страницу менеджера после сохранения заказа,
        если запрос был сделан с неё
        '''
        res = super().response_post_save_change(request, obj)
        if "next" in request.GET:
            url_allow = url_has_allowed_host_and_scheme(
                request.GET['next'],
                settings.ALLOWED_HOSTS
            )
            if url_allow:
                return HttpResponseRedirect(request.GET['next'])
        return 



class BoxAdmin(admin.TabularInline):
    model = Box
    extra = 0


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [BoxAdmin]

