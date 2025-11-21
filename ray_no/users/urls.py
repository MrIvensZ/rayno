from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView

from . import views

app_name = 'users'


urlpatterns = [
    path('registration', views.RegisterView.as_view(), name='registration'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit', views.ProfileUpdateView.as_view(), name='edit'),
    path('password_change', views.UserPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='password_change_done')
]
