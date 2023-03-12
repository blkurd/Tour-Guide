from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

#  _____________________________Trip CRUD_____________________________________________
class TripCreate(CreateView):
    model = Trip

    # fields here is an attribute and is required for a createview. It talk to the form and tells it to use all of its fields

    fields = '__all__'
    success_url = '/trips'

    # like this -----> fields = ["country", "location"] but using fields = '__all__' is best practice. 
    # success_url= '/trips/{trip_id}'


#  __________________________Experience CRUD_____________________________________________

class ExperienceCreate(CreateView):
    model = Experience
    fields = '__all__'

# Now we need to add a redirect when we make a success in making a form 
# or, we could redirect to the index page if we want
# success_url= '/experiences/{experience_id}'

class ExperienceUpdate(UpdateView):
    model = Experience  
    fields = ['expenses', 'description', 'location']
   



class ExperienceDelete(DeleteView):
    model = Experience
    