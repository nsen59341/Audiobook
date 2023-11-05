from django import forms
from .models import Audio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class PdfForm(forms.Form):
#     filename = forms.FileField()

class NewUserForm(UserCreationForm):
    # username & password are already required fields. UserCreationForm only requires username and password.
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    # Authentication
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PdfForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['name']
        widgets = {
            'name': forms.ClearableFileInput(attrs={'multiple':True})
        }
