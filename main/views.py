from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from main.forms import RegistrationForm
from .models import User

def home(request):
    return render(request, 'main/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.username = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'main/signup.html', {'form': form})

from .forms import EmailAuthenticationForm
def log_in(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = EmailAuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def profile(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.role =form.cleaned_data['role']
            user.save()
            return redirect('home')
    return render(request, 'profile.html', {'form': form,
                                                                'user': request.user})





