import io
from datetime import date, timedelta
from django.http import JsonResponse
from pytz import timezone

import qrcode
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from .models import Order, Box, Storage
from users.forms import UserCreationForm

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


def order_details(request, productid):
    if not request.user.is_authenticated:
        form = UserCreationForm()
        return render(request, "login.html", context={
            'form': form
        }
        )
    box = Box.objects.with_area().filter(number=productid)[0]
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


@csrf_exempt
def save_order(request):
    user = request.user
    order_details = request.body.decode('utf-8')
    Order.objects.create(
        renter=user,
        end_current_rent= date.today() + timedelta(days=30)
    )
    return JsonResponse({'status': 'ok','redirect': ''})


def view_storages(request):
    storages = Storage.objects.with_min_price().with_availability().all()

    return render(
        request,
        template_name='boxes.html',
        context={'storages': storages}
    )
