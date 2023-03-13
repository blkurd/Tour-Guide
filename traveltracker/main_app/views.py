from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Trip, Experience
from .forms import FeedingFrom

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

def add_feeding(request, experience_id):
    # create a ModelFrom instance from the data in request.POST
    form = FeedingFrom(request.POST)
    # After that, we need to validate the form, that means "does it match our data?"
    if form.is_valid():
        # we don't want to save the form to the db until is has the experience id
        new_feeding = form.save(commit=False)
        new_feeding.experience_id = experience_id 
        new_feeding.save()
    return redirect('detail', experience_id=experience_id)
# Below is a detail route for experiences 
# experience_id is defined, expecting an interger, in our url

def experience_detail(request, experience_id):
    experience = Experience.objects.get(id=experience_id)
# Here I am going to instantiate FeedingFrom to be rendered in the template 
    feeding_form = FeedingFrom()
    return render(request, 'experiences/experience_detail.html', { 'experience': experience, 'feeding_form' : feeding_form })



#  _____________________________Trip CRUD_____________________________________________
class TripCreate(CreateView):
    model = Trip

    # fields here is an attribute and is required for a createview. It talk to the form and tells it to use all of its fields
    fields = '__all__'
    success_url = '/trips'

    # like this -----> fields = ["country", "location"] but using fields = '__all__' is best practice. 
    # success_url= '/trips/{trip_id}'

class TripUpdate(UpdateView):
    model = Trip  
    fields = ['country']
    success_url='/trips'

class TripDelete(DeleteView):
    model = Trip
    success_url='/trips'


#  __________________________Experience CRUD_____________________________________________

class ExperienceCreate(CreateView):
    model = Experience
    fields = '__all__'
    success_url='/experiences'
    

# Now we need to add a redirect when we make a success in making a form 
# or, we could redirect to the index page if we want
# success_url= '/experiences/{experience_id}'

class ExperienceUpdate(UpdateView):
    model = Experience  
    fields = ['expenses', 'description', 'location']
    success_url='/experiences'


class ExperienceDelete(DeleteView):
    model = Experience
    success_url='/experiences'
