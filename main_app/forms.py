from django.forms import ModelForm 
from .models import Traveling

class TravelingForm(ModelForm):
    class Meta:
        model = Traveling 
        fields = ('date', 'mood')
