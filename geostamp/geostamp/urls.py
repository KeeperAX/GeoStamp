from django.contrib import admin
from django.urls import path, include
from users.views import register_view, login_view, logout_view
from places import views
from places.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),
    path('admin/', admin.site.urls),
    path('api/places/', views.places_api, name='places_api'),
    path('api/places/<int:pk>/', views.place_detail_api, name='place_detail_api'),
]