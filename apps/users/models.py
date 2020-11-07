from django.db import models
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

from apps.validators import REGEXPS


class CxUsernameValidator(UnicodeUsernameValidator):
    regex = REGEXPS['user']['username']


class CxUser(AbstractUser):
    """User app model extends django user model"""
    username_validator = CxUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Wymagane. Musi się skladac z dokladnie 5 liter.'),
        validators=[username_validator],
        error_messages={
            'unique': _("Uzytkownik o podanym loginie już istnieje!."),
        },
    )
    password = models.CharField(_('password'), max_length=128, validators=[validate_password])

    class Meta:
        verbose_name = 'Uzytkownik'
        verbose_name_plural = 'Uzytkownicy'
