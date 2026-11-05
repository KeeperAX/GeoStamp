import secrets

from django.db import models
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
    stamp_image = models.ImageField(upload_to='stamps/', blank=True, null=True, unique=True) #Фото заведения

    secret_key = models.CharField(max_length=8, unique=True, default=generate_place_code, editable=False,
                                  validators=[RegexValidator(regex=r'^[0-9]{8}$', message='Код состоит из 8 цифр')])
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name