from django.db import models
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from apps.user_texts import ERROR_MSG, MODEL_MSG
from apps.validators import CxUsernameValidator


class CxUser(AbstractUser):
    """User app model extends django user model."""
    username_validator = CxUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=MODEL_MSG['password'],
        validators=[username_validator],
        error_messages=ERROR_MSG['user']['username'],
    )
    password = models.CharField(_('password'), max_length=128, validators=[validate_password])

    class Meta:
        verbose_name = "Uzytkownik"
        verbose_name_plural = "Uzytkownicy"
