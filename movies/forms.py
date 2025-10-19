from django import forms
from .models import Petition, Rating

class PetitionForm(forms.ModelForm):
    class Meta:
        model= Petition
        fields= ["title", "description"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1,6)])
        }