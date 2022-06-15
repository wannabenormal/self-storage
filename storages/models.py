from django.db import models


class Storage(models.model):
    address = models.CharField('адрес', max_length=100, unique=True)
    temperature = models.SmallIntegerField('температура')
    ceiling_height = models.FloatField('Высота в метрах')


class Box(models.model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )
    number = models.CharField('номер', max_length=20)
    width = models.FloatField('ширина')
    length = models.FloatField('длина')
    height = models.FloatField('высота')


