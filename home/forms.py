
from .models import *
from django import forms



class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber  
        fields = ['email']
