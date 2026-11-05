from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Place

def serialize_place(place):
    return {
        "id": place.id,
        "name": place.name,
        "address": place.address,
        "street": place.street,
        "description": place.description,
        "rating": place.rating,
        "lat": place.latitude,
        "lon": place.longitude,
        "stamp_image": (place.stamp_image if place.stamp_image else None),
    }

def places_api(request):
    places = Place.objects.all()
    data = [serialize_place(p) for p in places]
    return JsonResponse(data, safe=False)
    
def place_detail_api(request, pk):
    place = get_object_or_404(Place, pk=pk)
    return JsonResponse(serialize_place(place))


def home_view(request):
    return render(request, 'home.html')