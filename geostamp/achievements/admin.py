from django.contrib import admin
from .models import Achievement, UserAchievement, UserStamp


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'condition', 'threshold', 'reward_points', 'is_active')

    list_filter = ('condition', 'is_active')
    search_fields = ('title', 'code')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    search_fields = ('user__name', 'achievement__title')
    list_select_related = ('user', 'achievement') #

    readonly_fields = ('user', 'achievement', 'earned_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UserStamp)
class UserStampAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'received_at')
    search_fields = ('user__name', 'place__name')
    list_select_related = ('user', 'place')

    readonly_fields = ('user', 'place', 'received_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

