from django import forms
from django.contrib.auth import authenticate, get_user_model


class RegistrationForm(forms.ModelForm):

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )

    class Meta:
        model = get_user_model()
        labels = {'password2': 'Введите пароль повторно'}
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password',
                  'password2',
                  'about_user',
                  'sex',
                  'email',
                  'avatar',
                  ]
        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter password'}),
        }

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password2'] != cleaned_data['password']:
            raise forms.ValidationError('пароли не совпадают!')
        return cleaned_data['password']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Wrong username or password')
        return cleaned_data


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['first_name',
                  'last_name',
                  'username',
                  'about_user',
                  'email',
                  'avatar',
                  ]
