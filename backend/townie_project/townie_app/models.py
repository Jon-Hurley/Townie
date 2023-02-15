from django.db import models

# Create your models here.
class Location(models.Model):
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)

class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, default='NULL')
    address = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)
