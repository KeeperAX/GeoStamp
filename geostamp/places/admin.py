from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = ("name", "address")

