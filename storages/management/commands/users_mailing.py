from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail

from storages.models import Order


def send_notes_about_end_of_rent(orders):
    messages = []
    for order in orders:
        box = order.boxes.first()
        if not box:
            continue
        if order.remaining_term.days in (3, 7, 14, 30):
            text = f'''Добрый день, {order.renter}! Напоминаем вам, что до
                   конца срока аренды помещения {box.number} по адресу
                   {box.storage} осталось {order.remaining_term.days} дней.
            '''
        elif order.remaining_term.days == 0:
            text = f'''Добрый день, {order.renter}! Срок аренды помещения
                   {box.number} по адресу {box.storage} подошел к концу.
                   Если планируете дальше пользоватсья нашими услугами,
                   продлите оплату аренды. В противном случае ваши вещи будут
                   храниться в течение 6 месяцев по повышенному тарифу.
                   Если в течении 6 месяцев вы их не заберёте, мы будем
                   вынуждены освободить помещение в одностороннем порядке.
            '''
        elif order.remaining_term.days in (-30, -60, -90, -120, -180):
            text = f'''Добрый день, {order.renter}! Напоминаем о необходимости
                   внести плату за аренду помещения {box.number} по адресу
                   {box.storage}.
            '''
        else:
            continue
        message = (
            'Аренда помещения в SelfStorage',
            text,
            None,
            [order.renter.email]
        )
        messages.append(message)
        return send_mass_mail(messages, fail_silently=False)


class Command(BaseCommand):
    help = 'Sends notifications to users'

    def handle(self, *args, **kwargs):
        orders = Order.objects.with_remaining_term() \
                              .select_related('renter') \
                              .prefetch_related('boxes')
        try:
            send_notes_about_end_of_rent(orders)
        except Exception as err:
            print(err)
