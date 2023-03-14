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

# A tuple of 2-tuples
TRANSPORTATION = (
    ('F', 'Air'),
    ('R', 'Car'),
    ('B', 'Bus'),
    ('T', 'Train'),
    ('S', 'Ship'),
    ('B', 'Bicycle')

)

# Add new Feeding model below Experience model
class Feeding(models.Model):
   date = models.DateField("Experience Date")
   transportation = models.CharField(
       max_length=1,
    # add the 'choices' field option
       choices=TRANSPORTATION,
    # set the default value for meal to be 'B'
       default=TRANSPORTATION[0][0]
   )

   # Add experience forign key reference
   # on_delete=models.CASCADE, means that when one experience is deleteld, all realted feedings are going to be deleted along with it. 
   experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

   def __str__(self):
      # Nice method for obtaining the friendly value of a Field.choice
      # Below< is a method from Django and it is produced like this: get_<name_of_field>_dispaly()
      return f"{self.get_transportation_display()} on {self.date}"

# This link is used to direct to the trip index page after submiting a form. 
# def get_absolute_url(self):
#     return reverse('trips', kwargs={'trip_id': self.id })

   def get_absolute_url(self):
      return reverse('experience_detail', kwargs={'experience_id': self.id })

# We can change the default sort by date, means that it will sort dates from newest to oldest and adding the oldest date to the bottom
# in the feeding choices by doing the following:
class Meta:
   ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for experience_id: {self.experience_id} @{self.url}"






  