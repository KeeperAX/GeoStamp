from django.http.response import JsonResponse
from django.shortcuts import render

from .models import Place
def places_api(request):
    places = Place.objects.all()
    data = [
        {
            "name": place.name,
            "lat": place.latitude,
            "lon": place.longitude,
            "rating": place.rating,
        } for place in places
        ]
    return JsonResponse(data, safe=False)
    
def home_view(request):
    return render(request, 'home.html')