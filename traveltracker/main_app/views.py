from django.shortcuts import render
from .models import Trip
from .models import Experience

# Create your views here.
# Define the home view


def home(request):
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def trips_index(request):
    trips = Trip.objects.all()
    return render(request, 'trips/index.html', {
    'trips': trips})


def experiences_index(request):
     experiences = Experience.objects.all()
     return render(request, 'experiences/experiences-index.html', {
     'experiences': experiences})

def experience_detail(request, experience_id):
    experience = Experience.objects.get(id=experience_id)
    return render(request, 'experiences/experience_detail.html', { 'experience': experience })

# trips = [
#   {'date': 13, 'country': 'Spain'},
#   {'date': 22, 'country': 'Italy'},
# ]





