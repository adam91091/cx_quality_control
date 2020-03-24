from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CxUser


class CxUserCreationForm(UserCreationForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')


class CxUserChangeForm(UserChangeForm):

    class Meta:
        model = CxUser
        fields = ('username', 'email')
