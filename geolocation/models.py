from django.db import models


class UserLocation(models.Model):
    ip = models.CharField('IP', max_length=15, unique=True)
    longitude = models.FloatField('долгота', blank=True, null=True)
    latitude = models.FloatField('широта', blank=True, null=True)


class StorageLocation(models.Model):
    longitude = models.FloatField('долгота', blank=True, null=True)
    latitude = models.FloatField('широта', blank=True, null=True)
    storage = models.OneToOneField(
        'storages.Storage',
        on_delete=models.CASCADE,
        related_name='location',
    )
