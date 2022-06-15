from django.db import models
from django.db.models import F, Min, Count, Q
from django.utils import timezone


class StorageQuerySet(models.QuerySet):
    def with_min_price(self):
        return self.annotate(
            min_price=Min('boxes__rental_price')
        )

    def with_availability(self):
        return self.annotate(
            empty_boxes=Count(
                'boxes',
                filter=Q(boxes__empty=True),
                distinct=True
            ),
            all_boxes=Count(
                'boxes',
                distinct=True
            )
        )


class Storage(models.Model):
    address = models.CharField('адрес', max_length=100, unique=True)
    temperature = models.SmallIntegerField('температура')
    ceiling_height = models.FloatField('Высота в метрах')
    feature = models.CharField('особенность', max_length=50, blank=True)
    contacts = models.CharField('Контакты', max_length=50, blank=True)
    description = models.TextField('Описание')
    objects = StorageQuerySet.as_manager()

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address


class BoxQuerySet(models.QuerySet):
    def with_area(self):
        return self.annotate(
            area=F('width') * F('length')
        )

    def empty(self):
        return self.filter(empty=True)

    def employed(self):
        return self.filter(empty=False)


class Order(models.Model):
    UNPROCCESSED = 'UN'
    ON_THE_WAY = 'OTW'
    DONE = 'D'
    STATUSES = (
        (UNPROCCESSED, 'Необработан'),
        (ON_THE_WAY, 'В пути'),
        (DONE, 'Завершён')
    )
    renter = models.ForeignKey(
        'users.User',
        verbose_name='заказчик',
        related_name='заказы',
        on_delete=models.CASCADE
    )
    need_delivery = models.BooleanField()
    address = models.CharField('адрес', max_length=100)
    status = models.CharField(
        'статус',
        max_length=10,
        choices=STATUSES,
        default=UNPROCCESSED,
        db_index=True
    )
    created_at = models.DateTimeField(
        'дата и время заказа',
        default=timezone.now,
        db_index=True
    )
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.renter} {self.address}'

class Box(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )
    # renter = models.ForeignKey() # добавлю когда будет модель юзера
    number = models.CharField('номер', max_length=20)
    floor = models.SmallIntegerField('этаж')
    width = models.FloatField('ширина')
    length = models.FloatField('длина')
    height = models.FloatField('высота')

    empty = models.BooleanField('свободно')
    rental_price = models.PositiveSmallIntegerField('Стоимость')
    start_current_rent = models.DateField(
        'Начало текущей аренды',
        null=True,
        blank=True
    )
    end_current_rent = models.DateField(
        'Конец текущей аренды',
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='boxes',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    objects = BoxQuerySet.as_manager()

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'боксы'

    def __str__(self):
        return self.number
