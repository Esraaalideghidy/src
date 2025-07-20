from .models import *
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'phone_number', 'comment']
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'review', 'email', 'phone_number']
