from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from main.forms import RegistrationForm
from .models import User

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'main/home.html'


from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import RegistrationForm

from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .tasks import send_welcome_email

class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        send_welcome_email.delay(user.email)

        login(self.request, user)
        return super().form_valid(form)

from .forms import EmailAuthenticationForm


from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
    template_name = 'main/login.html'
    authentication_form = EmailAuthenticationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})
        return form


from django.contrib.auth.views import LogoutView

class MyLogoutView(LogoutView):
    next_page = ''
    http_method_names = ['get', 'post']


from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView
from django.urls import reverse_lazy

class ProfileView(LoginRequiredMixin , UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'main/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user





