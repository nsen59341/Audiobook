from django import forms
from .models import Audio

# class PdfForm(forms.Form):
#     filename = forms.FileField()

class PdfForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['name']
        widgets = {
            'name': forms.ClearableFileInput(attrs={'multiple':True})
        }
