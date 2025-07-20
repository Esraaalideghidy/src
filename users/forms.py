from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email','subject', 'message']
          