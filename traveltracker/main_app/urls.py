from django.urls import path
from . import views

urlpatterns = [ 
# The name='home' kwarg gives the route a name. Naming a route is optional but is considered a best practice.
  path('', views.home, name='home'),

# view.about is from the view file, defined function

  path('about/', views.about, name='about'),

   path('trips/', views.trips_index, name='index'),

]
