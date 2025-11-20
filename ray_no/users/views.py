from django.contrib.auth import get_user_model, logout, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import EditProfileForm, RegistrationForm


user = get_user_model()


class RegisterView(CreateView):
    model = user
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class UserLoginView(views.LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    template = 'users/profile.html'
    return render(request, template, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = user
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')
