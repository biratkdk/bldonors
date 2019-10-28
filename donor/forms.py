from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Bloodreq, Contact, Donor, Payment, Stock

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

class Paymentform(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "donor_name",
            "email",
            "phone",
            "amount",
            "purpose",
            "payment_method",
            "remarks",
        ]

class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
