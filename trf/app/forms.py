from django import forms
from .models import Turf

class TurfBookingForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = ['name', 'email', 'game', 'date']
