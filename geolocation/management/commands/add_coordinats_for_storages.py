import json

from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail

from geolocation.models import StorageLocation
from storages.models import Storage


class Command(BaseCommand):
    help = 'Sends notifications to users'

    def handle(self, *args, **kwargs):
        with open('coordinates.json', 'r' ) as f:
            storages = json.load(f)
            for storage_data in storages:
                storage = Storage.objects.get(city=storage_data['city'])
                StorageLocation.objects.get_or_create(
                    storage=storage,
                    longitude=storage_data['lon'],
                    latitude=storage_data['lat']
                )