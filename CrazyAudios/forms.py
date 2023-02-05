from django import forms
from .models import Audio

class PdfForm(forms.Form):
    filename = forms.FileField()
