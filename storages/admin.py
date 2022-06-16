from django.contrib import admin
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.conf import settings
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Order, Box, Storage, StorageImage


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
        return res


class StorageBoxesInline(admin.TabularInline):
    model = Box
    fields = ['number', 'floor', 'width', 'length', 'height', 'rental_price']


class StorageImagesInline(SortableInlineAdminMixin, admin.TabularInline):
    model = StorageImage
    fields = ['image', 'preview_image', 'order']
    readonly_fields = ['preview_image']
    extra = 1

    def preview_image(self, obj):
        return format_html('<img src="{}" height="200"/>', obj.image.url)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [StorageImagesInline, StorageBoxesInline]
    search_fields = ['city', 'address']


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass
