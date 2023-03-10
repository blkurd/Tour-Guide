from django.contrib import admin
# import your models here
from .models import Trip
from .models import Experience

# Register your models here
admin.site.register(Trip)
admin.site.register(Experience)
