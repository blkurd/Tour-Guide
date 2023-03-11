from django.db import models
from django.urls import reverse

# Create your models here.

class Trip(models.Model):
   date = models.DateField()
   country = models.CharField(max_length=100) 


class Experience (models.Model):
   expenses = models.IntegerField() 
   description = models.TextField(max_length=500)
   location = models.CharField(max_length=100)

# This link is used to direct to the trip index page after submiting a form. 
# def get_absolute_url(self):
#     return reverse('trips', kwargs={'trip_id': self.id })

def get_absolute_url(self):
    return reverse('detail', kwargs={'experience_id': self.id })