from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CxUser
from apps.users.forms import CxUserCreationForm, CxUserChangeForm


class CxUserAdmin(UserAdmin):
    add_form = CxUserCreationForm
    form = CxUserChangeForm
    model = CxUser
    list_display = ['email', 'username']


admin.site.register(CxUser, CxUserAdmin)
