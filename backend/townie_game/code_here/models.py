from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)

    def __str__(self):
        return self.name

class Destination(models.Model):
    def __init__(self, location, name):
        self.name = name
        self.location = location