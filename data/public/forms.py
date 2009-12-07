from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

# class RegistrationForm(forms.Form):
#     username = forms.CharField(label="Username")
#     email = forms.EmailField(label="Email Address")
#     password = forms.CharField(label="Password", widget=forms.PasswordInput)
#     subscribed = forms.BooleanField(label="I would like to subscribe to your mailing list.", initial=False, required=False)
#     
#     def clean_username(self):
#         data = self.cleaned_data['username']
#         if User.objects.filter(username=data).count():
#             raise forms.ValidationError("Sorry, %s is already taken." % data)
#         return data

class CustomRegistrationForm(RegistrationForm):
    subscribed = forms.BooleanField(label="I would like to subscribe to your mailing list.", initial=False, required=False)