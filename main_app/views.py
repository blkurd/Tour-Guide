from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Trip, Experience, Photo
from .forms import FeedingFrom
import uuid  #This is a python package for creating unique identifiers. 
import boto3 # what we will use to connect s3
from django.conf import settings
# imports for signing up
# we want to automatically log in signed up users
from django.contrib.auth import login
# we want to use the builtin form for our custom view for sign up
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

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


@login_required
def trips_index(request):
    # Adding .filter(user=request.user) instead of .all is to let the user see what he can only creates and not what others create.
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trips/index.html', {
    'trips': trips})

@login_required
def experiences_index(request):
     # Adding .filter(user=request.user) instead of .all is to let the user see what he can only creates and not what others create.
     experiences = Experience.objects.filter(user=request.user)
     return render(request, 'experiences/experiences-index.html', {
     'experiences': experiences})

@login_required
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
@login_required
def experience_detail(request, experience_id):
    experience = Experience.objects.get(id=experience_id)
# Here I am going to instantiate FeedingFrom to be rendered in the template 
    feeding_form = FeedingFrom()
    return render(request, 'experiences/experience_detail.html', { 'experience': experience, 'feeding_form' : feeding_form })



#  _____________________________Trip CRUD_____________________________________________
class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    # fields here is an attribute and is required for a createview. It talk to the form and tells it to use all of its fields
    # the fields attribute is required for a createview. These inform the form
    # fields = '__all__'
    # we could also have written our fields like this:
    fields = ['date', 'country']
    success_url = '/trips'
    def form_valid(self, form):
        # we can assign the logged in user's data(id) to the experienc's create form
        form.instance.user = self.request.user

        return super().form_valid(form)



    # like this -----> fields = ["country", "location"] but using fields = '__all__' is best practice. 
    # success_url= '/trips/{trip_id}'

class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip  
    fields = ['country', 'date']
    success_url='/trips'

class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url='/trips'


#  __________________________Experience CRUD_____________________________________________

class ExperienceCreate(LoginRequiredMixin, CreateView):
    model = Experience
    # the fields attribute is required for a createview. These inform the form
    # fields = '__all__'
    # we could also have written our fields like this:
    fields = ['expenses', 'description', 'location']
    # we need to add redirects when we make a success
    success_url='/experiences'

    def form_valid(self, form):
        # we can assign the logged in user's data(id) to the experienc's create form
        form.instance.user = self.request.user

        return super().form_valid(form)
    

# Now we need to add a redirect when we make a success in making a form 
# or, we could redirect to the index page if we want
# success_url= '/experiences/{experience_id}'

class ExperienceUpdate(LoginRequiredMixin, UpdateView):
    model = Experience  
    fields = ['expenses', 'description', 'location']
    success_url='/experiences'


class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    success_url='/experiences'

@login_required
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

# # view for signup
# def signup(request):
#     # this view is going to be like our class based views
#     # because this is going to be able to handle a GET and a POST request
#     error_message = ''
#     if request.method == 'POST':
#         # this is how to create a user form object that includes data from the browser
#         form = UserCreationForm(request.POST)
#         # now we check validity of the form, and handle our success and error situations
#         if form.is_valid():
#             # we'll add the user to the database
#             user = form.save()
#             # then we'll log the user in
#             login(request, user)
#             # redirect to our index page
#             return redirect('experiences/experience-index')
#         else:
#             error_message = 'Invalid sign up - try again'
#     # a bad POST or GET request will render signup.html with an empty form
#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('experience-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



                          
                           
                            