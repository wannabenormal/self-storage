import io
import json
from datetime import date, timedelta

import qrcode
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

from storages.models import Order, Box


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
    return email.send(fail_silently=False)


@csrf_exempt
def save_order(request):
    user = request.user
    order_details = json.loads(request.body.decode('utf-8'))
    box = Box.objects.select_related('order').get(number=order_details['box'])
    if box.order and box.order.renter == user:
        box.order.end_current_rent = order_details['end_rent']
        box.order.save()
    else:
        order = Order.objects.create(
            renter = user,
            end_current_rent= date.today() + timedelta(days=30),
        )
        order.boxes.add(box)
        order.save()
    return JsonResponse({'message': 'ok','redirect': ''})


def end_rent(user, box_number):
    box = Box.objects.select_related('order').get(number=box_number)
    if box.order.renter == user:
        box.order = None
        box.save()
    return


@csrf_exempt
def open_box(request):
    user = request.user
    order_details = json.loads(request.body.decode('utf-8'))
    if order_details.get('end_rent'):
        end_rent(user, order_details.get('box'))
    message = f"""Добрый день {user.username}! Код доступа для окрытия вашего бокса.
              Если вы не запрашивали код, пожалуйста, обратитесь в службу поддержки:   
              8 (800) 000-00-00 """
    data_for_qr = 'https://dvmn.org'
    if send_qr_to_renter(data_for_qr, user.email, message):
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'message': 'something went wrong'})

