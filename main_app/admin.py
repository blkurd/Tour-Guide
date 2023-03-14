from django.contrib import admin
# import your models here
from .models import Trip, Experience, Feeding, Photo

# Register your models here
admin.site.register(Trip)
admin.site.register(Experience)
admin.site.register(Feeding)
admin.site.register(Photo)
