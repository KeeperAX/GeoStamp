from django.core.exceptions import ValidationError
from .models import Review, Visit


def create_review(user, place, rating, text=''):
    if not Visit.objects.filter(user=user, place=place).exists():
        raise ValidationError('Сначала подтвердите посещение заведения.')

    review = Review(user=user, place=place, rating=rating, text=text)
    review.full_clean()
    review.save()
    return review