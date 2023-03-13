from django.forms import ModelForm
from .models import Feeding

class FeedingFrom(ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'transportation']