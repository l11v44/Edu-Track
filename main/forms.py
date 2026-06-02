from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('guest', 'Guest'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'})
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name' , "email" , "role"]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

from django.contrib.auth.forms import AuthenticationForm
from django import forms

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True})
    )