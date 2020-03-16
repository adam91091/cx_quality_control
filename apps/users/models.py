from django.db import models
from django.contrib.auth.models import AbstractUser


class CxUser(AbstractUser):
    """This is custom django user model"""
    pass
