from django.shortcuts import render_to_response
from django import forms
from postcards.models import *

class PostcardForm(forms.ModelForm):
    class Meta:
        model = Postcard
    
    