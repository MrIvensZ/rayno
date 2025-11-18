from django.contrib.auth import get_user_model, authenticate, login, logout, views 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import EditProfileForm, RegistrationForm, LoginForm


user = get_user_model()


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    template = 'users/registration.html'
    context = {'form': form}
    return render(request, template, context)


# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             if user:
#                 login(request, user)
#                 return redirect('users:profile')
#     else:
#         form = LoginForm()

#     template = 'users/login.html'
#     context = {'form': form}
#     return render(request, template, context)

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


@login_required
def profile_edit(request):
    user = request.user
    form = EditProfileForm(request.POST or None,
                           files=request.FILES or None,
                           instance=user)
    template = 'users/edit_profile.html'
    context = {'form': form}
    if form.is_valid():
        form.save()
        url = reverse('users:profile')
        return redirect(url)
    return render(request, template, context)
