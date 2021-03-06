from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    def __str__(self):
        return (f"{self.id} {self.code} : {self.city}")

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    dest = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return (f" {self.id} - From {self.origin.city} to {self.dest.city} in {self.duration} hours ")


class Passenger(models.Model):
    f_Name = models.CharField(max_length=64)
    l_Name = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")
    def __str__(self):
        return f"{self.f_Name} {self.l_Name}"