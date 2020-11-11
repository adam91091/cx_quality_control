from django.test import TestCase

from apps.users.forms import CxUserAuthenticationForm
from apps.users.tests.factories import CxUserFactory


class CxUserLoginFormTest(TestCase):
    def setUp(self) -> None:
        self.user = CxUserFactory.create()
        self.login_form = {'username': self.user.username, 'password': self.user.password}

    def test_form_username_validation_negative(self):
        data = ['234', 'test', '14467']
        for value in data:
            self.login_form['username'] = value
            form = CxUserAuthenticationForm(data=self.login_form)
            self.assertFalse(form.is_valid(), msg=f"Value: {value}")

    def test_form_password_validation_negative(self):
        data = ['test', '-1', '22234333']
        for value in data:
            self.login_form['password'] = value
            form = CxUserAuthenticationForm(data=self.login_form)
            self.assertFalse(form.is_valid(), msg=f"Value: {value}")
