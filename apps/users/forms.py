from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm, \
    UsernameField
from django.utils.translation import gettext_lazy as _

from apps.users.models import CxUser
from apps.form_styles import USERNAME_STYLE, PASSWORD_STYLE


class CxUserCreationForm(UserCreationForm):
    class Meta:
        model = CxUser
        fields = ('username', )


class CxUserChangeForm(UserChangeForm):
    class Meta:
        model = CxUser
        fields = ('username', )


class CxUserAuthenticationForm(AuthenticationForm):
    validation_hints = {'username': "Login z pięciu pierwszych liter imienia i "
                                    "nazwiska (np. Jan Kowalski - jkowa).",
                        'password': "Przynajmniej 8 znakowe hasło z 1 cyfrą lub więcej.",
                        'lost_password': "Jeśli nie pamiętasz hasła, skontaktuj się z "
                                         "administratorem w celu zresetowania hasła.", }

    username = UsernameField(widget=forms.TextInput(attrs=USERNAME_STYLE))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs=PASSWORD_STYLE),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


class CxUserPasswordChangeForm(PasswordChangeForm):
    validation_hints = {'password': "Przynajmniej 8 znakowe hasło z 1 cyfrą lub więcej.", }

    old_password = forms.CharField(required=True, label='Stare hasło',
                                   widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                   error_messages={'required': 'To pole jest wymagane'})

    new_password1 = forms.CharField(required=True, label='Nowe hasło',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                    error_messages={'required': 'To pole jest wymagane'})

    new_password2 = forms.CharField(required=True, label='Nowe hasło (Powtórz)',
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                    error_messages={'required': 'To pole jest wymagane'})
