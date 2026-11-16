from django.core.exceptions import ValidationError
from .models import Review, Visit, Place
from django.db.models import Avg


def update_place_rating(place):
    res = Review.objects.filter(place=place)
    avg = res.aggregate(Avg('rating'))['rating__avg'] #среднее значение рейтинга
    if avg is None:
        place.rating = 0.0
    else:
        place.rating =round(avg, 1)
    place.save()


def create_place_visit(place, user, secret_key, visit_date):
    if place.secret_key != str(secret_key):
        raise ValidationError('Неверный 8-значный код заведения.')
    if Visit.objects.filter(user=user, place=place, visit_date__isnull=False).exists():
        raise ValidationError('Вы уже были в данном заведение.')

    visit = Visit(user=user, place=place, visit_date=visit_date)
    visit.save()
    return visit


def create_review(user, place, rating, text=''): #принимает уже готового пользователя
    if not Visit.objects.filter(user=user, place=place).exists():
        raise ValidationError('Сначала подтвердите посещение заведения.')
    if place.objects.filter(user=user, place=place).exists():
        raise ValidationError('Вы уже оставляли отзыв об этом заведении.')

    review = Review(user=user, place=place, rating=rating, text=text)
    review.full_clean()
    review.save()
    update_place_rating(place)
    return review