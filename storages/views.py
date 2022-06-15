import io

import qrcode
from django.core.mail import EmailMessage


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

