from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from .models import CxUser
from ..forms_utils import BASIC_REQ_STYLE, USERNAME_STYLE, PASSWORD_STYLE


class CxUserCreationForm(UserCreationForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')


class CxUserChangeForm(UserChangeForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')


class CxUserLoginForm(forms.ModelForm):
    validation_hints = {'username': "Login z pięciu pierwszych liter imienia i "
                                    "nazwiska (np. Jan Kowalski - jkowa).",
                        'password': "Przynajmniej 8 znakowe hasło z 1 cyfrą lub więcej."}

    class Meta:
        model = CxUser
        fields = ('username', 'password')

        labels = {
            'username': "Login",
            'password': "Hasło",
        }

        widgets = {
            'username': forms.TextInput(attrs={**USERNAME_STYLE, **{'style': 'width: 30%'}}),
            'password': forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
        }


class CxUserPasswordResetForm(SetPasswordForm):
    validation_hints = {'password': "Przynajmniej 8 znakowe hasło z 1 cyfrą lub więcej.", }

    new_password1 = forms.CharField(required=True, label='Nowe hasło',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
                                    error_messages={'required': 'To pole jest wymagane'})

    new_password2 = forms.CharField(required=True, label='Nowe hasło (Powtórz)',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
                                    error_messages={'required': 'To pole jest wymagane'})


class CxUserPasswordChangeForm(PasswordChangeForm):
    validation_hints = {'password': "Przynajmniej 8 znakowe hasło z 1 cyfrą lub więcej.", }

    old_password = forms.CharField(required=True, label='Stare hasło',
                                   widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
                                   error_messages={'required': 'To pole jest wymagane'})

    new_password1 = forms.CharField(required=True, label='Nowe hasło',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
                                    error_messages={'required': 'To pole jest wymagane'})

    new_password2 = forms.CharField(required=True, label='Nowe hasło (Powtórz)',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, **{'style': 'width: 30%'}}),
                                    error_messages={'required': 'To pole jest wymagane'})
