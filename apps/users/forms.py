from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CxUser
from ..forms_utils import BASIC_REQ_STYLE


class CxUserCreationForm(UserCreationForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')


class CxUserChangeForm(UserChangeForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')


class CxUserLoginForm(forms.ModelForm):
    validation_hints = {'username': "Nazwa użytkownika powinna składać się z 5 literowego skrótu imienia i nazwiska",
                        'password': "Hasło powinno składać się z przynajmniej 8 znaków"}

    class Meta:
        model = CxUser
        fields = ('username', 'password')

        labels = {
            'username': "Login",
            'password': "Hasło",
        }

        widgets = {
            'username': forms.TextInput(attrs={**BASIC_REQ_STYLE, **{'style': 'width: 30%'}}),
            'password': forms.PasswordInput(attrs={**BASIC_REQ_STYLE, **{'style': 'width: 30%'}}),
        }
