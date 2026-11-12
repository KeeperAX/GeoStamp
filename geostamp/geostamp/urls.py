from django.contrib import admin
from django.urls import path, include
from users.views import register_view, login_view, logout_view
from places import views
from places.views import home_view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),
    path('admin/', admin.site.urls),
    path('api/places/', views.places_api, name='places_api'),
    path('api/places/<int:pk>/', views.place_detail_api, name='place_detail_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)