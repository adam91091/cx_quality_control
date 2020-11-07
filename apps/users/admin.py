from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CxUser
from apps.users.forms import CxUserCreationForm, CxUserChangeForm


class CxUserAdmin(UserAdmin):
    add_form = CxUserCreationForm
    form = CxUserChangeForm
    model = CxUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'group']

    @staticmethod
    def group(obj):
        """
        get group, separate by comma, and display empty string if user has no group
        """
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''


admin.site.register(CxUser, CxUserAdmin)
