from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 border border-gray-200 rounded-xl'}),
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match!")
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



class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, label="Enter your 6-digit code")