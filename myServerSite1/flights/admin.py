from django.contrib import admin
from flights.models import Flight,Airport, Passenger

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)
