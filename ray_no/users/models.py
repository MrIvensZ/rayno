from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = [('1', 'Male'), ('2', 'Female')]


class CustomUser(AbstractUser):
    about_user = models.TextField(max_length=128,
                                  verbose_name='О себе')
    sex = models.CharField(max_length=6,
                           choices=CHOICES,
                           null=True,
                           verbose_name='Пол')

    avatar = models.ImageField(upload_to='user_avatars',
                               blank=True,
                               null=True,
                               verbose_name='Аватар пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
