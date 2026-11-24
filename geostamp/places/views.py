import json
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Place, Review, Visit
from users.register_forms import LoginForm, UserRegisterForm
from users.models import User
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from users.register_forms import LoginForm, UserRegisterForm
from .services import create_review, create_place_visit

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
        "stamp_image": (place.stamp_image.url if place.stamp_image else None),
    }

#API-представление для выдачи списка всех заведений (используется скриптом карты)
def places_api(request):
    places = Place.objects.all() #все заведения из базы
    data = [serialize_place(p) for p in places] #берем заведения из базы
    return JsonResponse(data, safe=False)

# API-представление для получения детальной информации об одном заведении и его отзывах
def place_detail_api(request, pk):
    place = get_object_or_404(Place, pk=pk) #заведение по пк
    data = serialize_place(place)

    reviews = Review.objects.filter(place=place).select_related()  #поиск всех отзывово к заведению и пользователей к ним
    data['reviews'] = [{
        "user_name": r.user.name,  # Было r_user.name
        "rating": r.rating,  # Было r_rating
        "text": r.text,
        'created_at': r.created_at.strftime('%d.%m.%Y %H:%M')
    }
        for r in reviews]
    # Проверяем сессию текущего пользователя
    user_id = request.session.get('user_id')
    data['is_authenticated'] = bool(user_id)
    if user_id:
        data['has_visited'] = Visit.objects.filter(user_id=user_id, place=place).exists()
        data['has_reviewed'] = Review.objects.filter(user_id=user_id, place=place).exists()
    else:
        data['has_visited'] = False
        data['has_reviewed'] = False

    return JsonResponse(data)  # Возвращаем всю собранную информацию в виде JSON

#Представление для подтверждения посещения (чекин по 8-значному коду)
@require_POST
def checkin_place_api(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Войдите в аккаунт для подтверждения посещения.'}, status=403)

    user = get_object_or_404(User, pk=user_id)
    place = get_object_or_404(Place, pk=pk)

    try:
        body = json.loads(request.body)
        secret_key = body.get('secret_key', '')
        create_visit(user=user, place=place, secret_key=secret_key)
        return JsonResponse({'status': 'ok', 'message': 'Посещение подтверждено! Теперь вы можете оставить отзыв.'}, status=201)
    except ValidationError as e:
        msg = e.messages[0] if hasattr(e, 'messages') else str(e)
        return JsonResponse({'error': msg}, status=400)

@require_POST
def add_review_api(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Войдите в аккаунт, чтобы оставить отзыв.'}, status=403)

    user = get_object_or_404(User, pk=user_id)
    place = get_object_or_404(Place, pk=pk)

    try:
        body = json.loads(request.body)
        rating = int(body.get('rating', 0))
        text = body.get('text', '').strip()
        create_review(user=user, place=place, rating=rating, text=text)
        return JsonResponse({'status': 'ok', 'rating': place.rating}, status=201)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Укажите корректную оценку от 1 до 5.'}, status=400)
    except ValidationError as e:
        msg = e.messages[0] if hasattr(e, 'messages') else str(e)
        return JsonResponse({'error': msg}, status=400)

def home_view(request):
    # Передаем пустые формы для модальных окон фронтендера на главной странице
    return render(request, 'home.html', {
        'avt': LoginForm(),
        'reg': UserRegisterForm(),
    })