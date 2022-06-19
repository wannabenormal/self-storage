from datetime import date, datetime
from django.db import models
from django.db.models import F, Min, Count, Q, Sum
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
                filter=Q(boxes__order=None),
                distinct=True
            ),
            all_boxes=Count(
                'boxes',
                distinct=True
            )
        )


class Storage(models.Model):
    city = models.CharField('город', max_length=50)
    address = models.CharField('адрес', max_length=100)
    temperature = models.SmallIntegerField('температура')
    ceiling_height = models.FloatField('Высота в метрах')
    feature = models.CharField('особенность', max_length=50, blank=True)
    contacts = models.CharField('Контакты', max_length=50, blank=True)
    description = models.TextField('Описание', blank=True)
    driving_directions = models.TextField('Схема проезда', blank=True)

    objects = StorageQuerySet.as_manager()

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city}, {self.address}'


class StorageImage(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='Порядок')
    image = models.ImageField(verbose_name='Изображение')
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='склад'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order} {self.storage}'


class BoxQuerySet(models.QuerySet):
    def with_area(self):
        return self.annotate(
            area=F('width') * F('length')
        )

    def to_3(self):
        return self.annotate(
            area=F('width') * F('length')
        ).filter(
            area__lte=3
        )

    def to_10(self):
        return self.annotate(
            area=F('width') * F('length')
        ).filter(
            area__lte=10
        )

    def from_10(self):
        return self.annotate(
            area=F('width') * F('length')
        ).filter(
            area__gte=10
        )


class OrderQuerySet(models.QuerySet):
    def with_cost(self):
        return self.annotate(
            cost=Sum('boxes__rental_price')
        )

    def expired(self):
        current_date = datetime.now()
        return self.filter(end_current_rent__lt=current_date)


class Order(models.Model):
    UNPROCCESSED = 'UN'
    ON_THE_WAY = 'OTW'
    DONE = 'D'
    STATUSES = (
        (UNPROCCESSED, 'Необработан'),
        (ON_THE_WAY, 'В пути'),
        (DONE, 'Завершён'),
    )
    renter = models.ForeignKey(
        'users.User',
        verbose_name='заказчик',
        related_name='orders',
        on_delete=models.CASCADE
    )
    need_delivery = models.BooleanField('нужна доставка?', default=False)
    address = models.CharField('адрес', max_length=100, blank=True)
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
    start_current_rent = models.DateField(
        'Начало текущей аренды',
        default=timezone.now,
    )
    end_current_rent = models.DateField(
        'Конец текущей аренды',
    )

    objects = OrderQuerySet.as_manager()

    @property
    def get_delay(self):
        return (self.end_current_rent - date.today()).total_seconds() // 86400

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
    number = models.CharField(
        'номер',
        max_length=20,
        unique=True,
    )
    floor = models.SmallIntegerField('этаж')
    width = models.FloatField('ширина')
    length = models.FloatField('длина')
    height = models.FloatField('высота')

    rental_price = models.PositiveSmallIntegerField('Стоимость')
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
