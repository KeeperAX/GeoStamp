from django.db import models
from django.core.validators import MinValueValidator


class Achievement(models.Model):
    class Condition(models.TextChoices): # типы условий достижений
        STAMPS = 'stamps', 'Количество штампов'
        REVIEWS = 'reviews', 'Количество отзывов'

    code = models.SlugField(max_length=60, unique=True) # человекочитаемый идентификатор в URL
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')

    condition = models.CharField(max_length=20, choices=Condition.choices)
    threshold = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    reward_points = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='recipients')

    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'achievement'],name='unique_user_achievement')]

    def __str__(self):
        return f'{self.user.name} — {self.achievement.title}'


class UserStamp(models.Model):
    user = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='stamps')
    place = models.ForeignKey('places.Place',on_delete=models.CASCADE,related_name='collected_stamps')

    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'place'],name='unique_user_place_stamp')]

    def __str__(self):
        return f'{self.user.name} — {self.place.name}'