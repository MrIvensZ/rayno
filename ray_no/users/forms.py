from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите имя пользователя'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'password1',
                  'password2',
                  'about_user',
                  'sex',
                  'avatar',
                  ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Введите вашу фамилию'}),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@mail.com'}),
            'about_user': forms.Textarea(attrs={
                'placeholder': 'Расскажите о себе'})
            }


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

    username = forms.CharField(
        disabled=True,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите имя пользователя'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email',
                  'first_name', 'last_name',
                  'about_user', 'avatar',]
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@mail.com'}),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Введите вашу фамилию'}),
            'about_user': forms.Textarea(attrs={
                'placeholder': 'Расскажите о себе'})
            }
