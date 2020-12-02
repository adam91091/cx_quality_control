from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm, \
    UsernameField

from apps.user_texts import HINTS, ERROR_MSG, LABELS
from apps.users.models import CxUser
from apps.form_styles import USERNAME_STYLE, PASSWORD_STYLE


class CxUserCreationForm(UserCreationForm):
    """Customize user creation form in django admin."""
    class Meta:
        model = CxUser
        fields = ('username', )


class CxUserChangeForm(UserChangeForm):
    """Customize user update form in django admin."""
    class Meta:
        model = CxUser
        fields = ('username', )


class CxUserAuthenticationForm(AuthenticationForm):
    """Customize user login form & add hint
    messages for client side validation."""
    validation_hints = HINTS['user']

    username = UsernameField(widget=forms.TextInput(attrs=USERNAME_STYLE))
    password = forms.CharField(
        label=LABELS['user']['password'],
        strip=False,
        widget=forms.PasswordInput(attrs=PASSWORD_STYLE),
    )

    error_messages = ERROR_MSG['user']['username']


class CxUserPasswordChangeForm(PasswordChangeForm):
    """Provide form for user password changing in user profile."""
    validation_hints = HINTS['user']

    old_password = forms.CharField(required=True, label=LABELS['user']['old_password'],
                                   widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                   error_messages=ERROR_MSG['user']['password'])

    new_password1 = forms.CharField(required=True, label=LABELS['user']['new_password'],
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                    error_messages=ERROR_MSG['user']['password'])

    new_password2 = forms.CharField(required=True, label=LABELS['user']['new_password_confirm'],
                                    widget=forms.PasswordInput(attrs={**PASSWORD_STYLE, }),
                                    error_messages=ERROR_MSG['user']['password'])
