import requests
from geopy import distance

from .models import UserLocation, StorageLocation
from storages.models import Storage


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_coordinats_by_ip(ip):
    url = f'http://ipwho.is/{ip}'
    params = {
        'fields': 'latitude,longitude',
        'output': 'json'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response.json())
    return response.json()
    

def get_nearest_storage(request):

    user_ip = get_client_ip(request)
    if not user_ip:
        return Storage.objects.first()

    user_location, created = UserLocation.objects.get_or_create(
        ip=user_ip
    )
    if created:
        coordinats = get_coordinats_by_ip(user_ip)
        user_location.latitude = coordinats['latitude']
        user_location.longitude = coordinats['longitude']
        user_location.save()
    
    distances = []
    storages_location = StorageLocation.objects.all()
    for storage_location in storages_location:
        place_distance = distance.distance(
            (user_location.latitude, user_location.longitude),
            (storage_location.latitude, storage_location.longitude)
        ).kilometers
        distances.append((storage_location.storage, place_distance))
    sorted_distances = sorted(distances, key=lambda x: x[1])
    if sorted_distances:
        return sorted_distances[0][0]
    return Storage.objects.first()
    