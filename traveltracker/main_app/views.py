from django.shortcuts import render
import datetime

# Create your views here.
# Define the home view


def home(request):
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def trips_index(request):
    return render(request, 'trips/index.html', {
    'trips': trips
  })


trips = [
  {'date': 13, 'country': 'Spain'},
  {'date': 22, 'country': 'Italy'},
]





