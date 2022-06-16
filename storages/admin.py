from django.contrib import admin
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect
from django.conf import settings
from django import forms

from .models import Order, Box, Storage


class BoxInline(admin.TabularInline):
    model = Box
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('renter',)
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



@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [BoxInline,]

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass