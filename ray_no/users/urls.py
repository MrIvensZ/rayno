from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('registration', views.RegisterView.as_view(), name='registration'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit', views.ProfileUpdateView.as_view(), name='edit'),
]
