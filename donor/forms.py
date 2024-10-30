from django.core import validators
from django import forms
from django.db.models import fields
from django.db.models.fields import files
from .models import Bloodreq, Contact, Donor, Stock
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Donorform(forms.ModelForm):
    class Meta :
        model = Donor
        fields = '__all__'
    
class Bloodreqform(forms.ModelForm):
    class Meta:
        model = Bloodreq
        fields = '__all__'

class Stockform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
    
class Contactform(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']