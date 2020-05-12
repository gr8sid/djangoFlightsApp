from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from flights.models import Flight,Airport

# Create your views here.
def index(request):
    # return HttpResponse("Hello, This is the Flights Page.");
    context = {"flights": Flight.objects.all(), "airports": Airport.objects.all()}
    return render(request, "flights/index.html", context)
    

def flight(request, flight_id):
    try:
        f = Flight.objects.get(pk = flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does NOT exist!!!")
    
    context = {"flights": f}
    return render(request, "flights/flight.html", context)
