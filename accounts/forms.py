import requests
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import UserProfile

class CustomErrorList(ErrorList):
 def __str__(self):
    if not self:
        return ''
    return mark_safe(''.join([ f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))
  
class CustomUserCreationForm(UserCreationForm):
    city= forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control','placeholder': 'City'
    }))
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update( {'class': 'form-control'})
    
    def save(self, commit=True):
        user= super().save(commit)
        city= self.cleaned_data.get('city')
        if city:
            profile= user.userprofile
            profile.city= city
            
            #Geocoding the city
            try:
                url= "https://maps.googleapis.com/maps/api/geocode/json"
                params= {"address": city, "key": settings.GOOGLE_MAPS_API_KEY}
                response=requests.get(url, params= params).json()
                if response["status"]=="OK":
                    location= response["results"][0]["geometry"]["location"]
                    profile.latitude= location["lat"]
                    profile.longitude= location["lng"]
            except Exception as e:
                print(f"Geocoding failed: {e}")
            profile.save()
        return user