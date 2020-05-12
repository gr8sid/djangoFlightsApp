from django.contrib import admin
from flights.models import Flight,Airport

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
