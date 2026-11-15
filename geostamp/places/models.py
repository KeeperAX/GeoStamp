import secrets

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

def generate_place_code():
    return f'{secrets.randbelow(100000000):08d}'


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    street = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    stamp_image = models.ImageField(upload_to='stamps/', blank=True, null=True, unique=True) # Фото заведения

    secret_key = models.CharField(max_length=8, unique=True, default=generate_place_code, editable=False,
                                  validators=[RegexValidator(regex=r'^[0-9]{8}$', message='Код состоит из 8 цифр')])
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Visit(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)
    visit_date = models.DateField(default=timezone.localdate)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'place', 'visit_date'],
                name='unique_daily_visit'
            )
        ]

    def __str__(self):
        return f'{self.user.name} — {self.place.name}'

class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'place'],
                name='unique_user_place_review'
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name='review_rating_from_1_to_5'
            ),
        ]

    def __str__(self):
        return f'{self.user.name} — {self.place.name}: {self.rating}'