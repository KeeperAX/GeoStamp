from django.db import models

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField()
    address = models.TextField(max_length=100)
    secret_key = models.IntegerField(unique=True)
    rating = models.FloatField(default=0.0, max_length=5)
    latitude = models.FloatField() 
    longitude = models.FloatField()

    #Leaflet