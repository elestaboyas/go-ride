from django import forms
from .models import Ride
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup_location', 'dropoff_location']
        widgets = {
            'pickup_location': forms.TextInput(attrs={'placeholder': 'Enter pickup location'}),
            'dropoff_location': forms.TextInput(attrs={'placeholder': 'Enter drop-off location'}),
        }


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

