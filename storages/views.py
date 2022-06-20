from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from .models import Order, Box, Storage
from geolocation.views import get_nearest_storage
from users.forms import UserCreationForm


def is_manager(user):
    return user.is_staff


@user_passes_test(is_manager, login_url='signin')
def view_orders(request):
    orders = Order.objects.exclude(status='D') \
                          .filter(need_delivery=True) \
                          .with_cost() \
                          .select_related('renter')

    return render(
        request,
        template_name='order_items.html',
        context={'order_items': orders}
    )


@user_passes_test(is_manager, login_url='signin')
def view_expired_orders(request):
    orders = Order.objects.expired() \
                          .prefetch_related('boxes') \
                          .select_related('renter') \
                          .order_by('end_current_rent')
    for order in orders:
        order.number_of_boxes = [box.number for box in order.boxes.all()]
    return render(
        request,
        template_name='expired_orders.html',
        context={'order_items': orders}
    )


@user_passes_test(is_manager, login_url='signin')
def view_manager_menu(request):
    return render(request, template_name='manager.html')


def order_details(request, product_number):
    if not request.user.is_authenticated:
        form = UserCreationForm()
        return render(
            request,
            "login.html",
            context={'form': form}
        )
    box = Box.objects.with_area().filter(number=product_number)[0]
    if request.GET.get('prolong'):
        start_current_rent = box.order.start_current_rent
        end_current_rent = box.order.end_current_rent + timedelta(days=30)
    else:
        start_current_rent = date.today()
        end_current_rent = start_current_rent + timedelta(days=30)
    return render(
        request,
        template_name='order_details.html',
        context={
            'box': box,
            'start_rent': start_current_rent,
            'end_rent': end_current_rent
        }
    )


def view_storages(request):
    storages = Storage.objects.with_min_price() \
                              .with_availability() \
                              .all()

    return render(
        request,
        template_name='boxes.html',
        context={'storages': storages}
    )


def view_index(request):
    nearest_storage = get_nearest_storage(request)
    nearest_storage = Storage.objects.with_min_price() \
                             .with_availability() \
                             .filter(pk=nearest_storage.pk)[0]
    return render(
        request,
        template_name='index.html',
        context={'nearest_storage': nearest_storage}
    )
