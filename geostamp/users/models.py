from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique= True, null=False)
    email = models.EmailField(max_length = 50, unique= True, null = False)
    password = models.CharField(max_length=64, null=False)
    email_confirmed = models.BooleanField(default = False) #Активированна ли почта
    registered_on = models.DateTimeField(auto_now_add = True)


