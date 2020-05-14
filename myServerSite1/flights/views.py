from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from flights.models import Flight,Airport, Passenger
from django.contrib.auth import authenticate, login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import FlightSerializer
import requests
import datetime
import arrow



# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "flights/login.html", {"message": None})
    
    context = {"users" : request.user, "flights": Flight.objects.all(), "airports": Airport.objects.all()}
    return render(request, "flights/index.html", context)
    

def flight(request, flight_id):
    try:
        f = Flight.objects.get(pk = flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does NOT exist!!!")
    
    context = {
        "flights": f, 
        "passengers": f.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=f).all()
        }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        pass_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=pass_id)
        flight = Flight.objects.get(pk=flight_id)
        # console.log("******" + pass_id + " - " + passenger + " - " + flight)
    except KeyError:
        return render(request, "flights/error.html",{"message": "Passenger Not Selected!"} )
    except Flight.DoesNotExist:
        raise Http404(request, "flights/error.html",{"message":"NO Flight!!"} )
    except Passenger.DoesNotExist:
        raise Http404(request, "flights/error.html",{"message":"NO Passenger!!"} )

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight",args=(flight_id,)))

def login_view(request):
    uname = request.POST["username"]
    pswd = request.POST["password"]
    user = authenticate(request, username=uname, password=pswd)

    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/login.html", {"message": "Invalid Credentials!"})

def logout_view(request):
    logout(request)
    return render(request, "flights/login.html", {"message": "User Logged Out!"})

# Requesting API:
class FlightList(APIView):

    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def post(self):
        pass

def covid(request):
    response = requests.get('https://api.covid19api.com/total/country/canada')
    indiaCases = response.json()
    cases = indiaCases[-1]['Confirmed']
    active = indiaCases[-1]['Active']
    recovered = indiaCases[-1]['Recovered']
    deaths = indiaCases[-1]['Deaths']
    # date = indiaCases[-1]['Date'].date()

    date_time_str = indiaCases[-1]['Date']
    # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    # date = date_time_obj.date()

    dt = arrow.get(date_time_str)
    date = dt.date()

    return render(request, 'flights/covid.html', {
        "indiaCases": indiaCases[-1], 
        "confirmed": cases,
        "active": active,
        "recovered": recovered,
        "deaths": deaths,
        "date": date,
        })
    # {
    #     # 'Country': indiaCases['Country'],
    #     # 'Confirmed': indiaCases['Confirmed'],
    #     # 'Deaths': indiaCases['Deaths'],
    #     # 'Recovered': indiaCases['Recovered'],
    #     # 'Active': indiaCases['Active'],
    #     # 'Date': indiaCases['Date'],
        
    # }
    