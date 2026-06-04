from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))
    ROLE_CHOICES = [
        ('S', 'Student'),
        ('T', 'Teacher'),
        ('G', 'Guest'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500 outline-none'
            })
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True})
    )




class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition'
            })
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']