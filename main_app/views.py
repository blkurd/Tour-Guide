from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Trip, Experience, Photo
from .forms import FeedingFrom
import uuid  #This is a python package for creating unique identifiers. 
import boto3 # what we will use to connect s3
from django.conf import settings

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL


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
    return redirect('experience_detail', experience_id=experience_id)

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


def add_photo(request, experience_id):
    # photo_file will be the name attribute of our form input
    # input type will be file 
    photo_file = request.FILES.get('photo-file', None)
     # use conditional logic to make sure a file is present
    if photo_file: 
        # This accesses the s3 bucket and use it to create a reference to the boto3 client
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # This line below is for creating a unique key for our photos
        # create a unique key for our photos
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # We are going to use try ... except which is just like try .... catch in js
        # to handle the situation if anything should go wrong
        try:
            # if success, it upload the photo file
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            # build the full url string to upload to s3
            url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
            # if our upload(that used boto3) was successful 
            # we want to use that photo location to create a Photo model
            photo = Photo(url=url, experience_id=experience_id)
            # save the instance to the db = database
            photo.save()
        except Exception as error:
            # print an error message
            print('Error uploading photo', error)
            return redirect('experience_detail', experience_id=experience_id)
    # upon success redirect to detail page
    return redirect('experience_detail', experience_id=experience_id)

                          
                           
                            