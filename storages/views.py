import io

import qrcode
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from .models import Order, Storage

def send_qr_to_renter(data_for_qr:str, renter_email, message):
    '''
    Генерирует qr из параметра data_for_qr, отправляет на почту renter_email,
    с текстом message. При успешной отправке возвращает 1
    '''
    
    code = qrcode.make(data_for_qr)
    im_resize = code.resize((500, 500))
    buf = io.BytesIO()
    im_resize.save(buf, format='png')
    byte_im = buf.getvalue()
    email = EmailMessage(
        subject='Код доступа',
        body=message,
        to=(renter_email,)
    )
    email.attach('code.png', byte_im)
    return email.send()


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


def view_storages(request):
    storages = Storage.objects.with_min_price().with_availability().all()

    return render(
        request,
        template_name='boxes.html',
        context={'storages': storages}
    )
