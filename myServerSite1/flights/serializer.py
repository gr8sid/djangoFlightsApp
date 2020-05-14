from rest_framework import serializers
from .models import Flight, Passenger, Airport

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('origin','dest')
