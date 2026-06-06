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
from .tasks import send_verification_email
from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
import random
from django.shortcuts import render, redirect
class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.save()
        send_verification_email.delay(user.email, code)
        self.request.session['email_to_verify'] = user.email
        return redirect('verify_code')

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

import random
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import VerificationForm
from .models import User
from .tasks import send_verification_email
class VerifyCodeView(FormView):
    form_class = VerificationForm
    template_name = 'main/verify.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_code = form.cleaned_data['code']
        email = self.request.session.get('email_to_verify')

        try:
            user = User.objects.get(email=email)
            if user.verification_code == user_code:
                user.is_active = True
                user.verification_code = None
                user.save()
                login(self.request, user)
                return super().form_valid(form)
            else:
                form.add_error('code', 'Invalid verification code.')
                return self.form_invalid(form)
        except User.DoesNotExist:
            return redirect('signup')