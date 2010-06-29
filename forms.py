from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    comment = forms.CharField(label='Comment', widget=forms.Textarea)