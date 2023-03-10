from django.db import models

# Create your models here.

class Trip(models.Model):
   date = models.DateField()
   country = models.CharField(max_length=100) 


class Experience (models.Model):
   expenses = models.IntegerField() 
   description = models.TextField(max_length=500)
   location = models.CharField(max_length=100)