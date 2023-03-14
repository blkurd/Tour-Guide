from django.urls import path
from . import views

urlpatterns = [ 
# The name='home' kwarg gives the route a name. Naming a route is optional but is considered a best practice.
  path('', views.home, name='home'),

# view.about is from the view file, defined function

  path('about/', views.about, name='about'),

# ____________________________________________________________Trip paths_______________________________________________________________

  path('trips/', views.trips_index, name='trips'),

  path('trips/create/', views.TripCreate.as_view(), name='trip-create'),

  path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name='trip-update'),

  path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trip-delete'),


# _______________________________________________________________Experience paths________________________________________________________

  path('experiences/', views.experiences_index, name='experience-index'),

  path('experiences/create/', views.ExperienceCreate.as_view(), name='experience-create'),
  
  path('experiences/<int:pk>/update/', views.ExperienceUpdate.as_view(), name='experience-update'),

  path('experiences/<int:pk>/delete/', views.ExperienceDelete.as_view(), name='experience-delete'),

  path('experiences/<int:experience_id>/', views.experience_detail, name='experience_detail'),

# Feedings for experience 

  path('experiences/<int:experience_id>/add_feeding/', views.add_feeding, name='add_feeding'),

# Experience path for photo

  path('experiences/<int:experience_id>/add_photo/', views.add_photo, name='add_photo'),  

]
