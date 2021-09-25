from django import forms
from django.forms import widgets

class Search(forms.Form):
    title = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "placeholder": "Search" 
        }))
