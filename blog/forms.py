from .models import *



from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email','subject' , 'message']



