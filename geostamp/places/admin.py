from django.contrib import admin
from .models import Place, Visit, Review


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = ("name", "address")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'place', 'visit_date', 'visited_at')
    readonly_fields = ('user', 'place', 'visit_date', 'visited_at')

    @admin.display(description='Пользователь')
    def user_name(self, obj):
        return obj.user.name

    def has_add_permission(self, request):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'place', 'rating', 'created_at')
    readonly_fields = ('user', 'place', 'rating', 'text', 'created_at')

    @admin.display(description='Пользователь')
    def user_name(self, obj):
        return obj.user.name

    def has_add_permission(self, request):
        return False