from django import forms

from .models import Rating, Movies


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['rate',]
        labels = {'rate': 'Ваша оценка:'}
        widgets = {
            'rate': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
            })
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['title',
                  'release_date',
                  'director',
                  'genre',
                  'poster']
        widgets = {
            'release_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }
