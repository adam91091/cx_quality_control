from django.db import models

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
        help_text=_('Required. Exactly 5 characters only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
