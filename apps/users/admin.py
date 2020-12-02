from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CxUser
from apps.users.forms import CxUserCreationForm, CxUserChangeForm


class CxUserAdmin(UserAdmin):
    """Django admin user list view customization."""
    add_form = CxUserCreationForm
    form = CxUserChangeForm
    model = CxUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'group']

    @staticmethod
    def group(user: CxUser) -> str:
        """Display user groups as a string separated by commas
        or display empty string if user has no groups.
        """
        return ','.join([g.name for g in user.groups.all()]) if user.groups.count() else ''


admin.site.register(CxUser, CxUserAdmin)
