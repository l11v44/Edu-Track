from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from main.forms import RegistrationForm
from .models import User

def home(request):
    return render(request, 'main/home.html')


from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            from .models import User
            if User.objects.filter(username=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.username = email
                user.save()
                auth_login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'main/signup.html', {'form': form})

from .forms import EmailAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = EmailAuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})

    return render(request, 'main/login.html', {'form': form})

def logout_(request):
    logout(request)
    return redirect('home')
from .forms import ProfileForm
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'main/profile.html', {'form': form})





