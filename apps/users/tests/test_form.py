from django.test import TestCase

from apps.users.forms import CxUserLoginForm
from apps.users.tests import PASSWORD
from apps.users.tests.factories import CxUserFactory


class CxUserLoginFormTest(TestCase):
    def setUp(self) -> None:
        self.user = CxUserFactory.create()
        self.login_form = {'username': 'admin', 'password': PASSWORD}

    def test_form_username_validation_positive(self):
        self.login_form['username'] = 'testk'
        form = CxUserLoginForm(data=self.login_form, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_username_validation_negative(self):
        data = ['234', 'test', '14467']
        for value in data:
            self.login_form['username'] = value
            form = CxUserLoginForm(data=self.login_form, instance=self.user)
            self.assertFalse(form.is_valid(), msg=f"Value: {value}")

    def test_form_password_validation_positive(self):
        data = ['1abdok44q', '1111111o']
        for value in data:
            self.login_form['password'] = value
            form = CxUserLoginForm(data=self.login_form, instance=self.user)
            self.assertTrue(form.is_valid(), msg=f"Value: {value}")

    def test_form_password_validation_negative(self):
        data = ['test', '-1', '22234333']
        for value in data:
            self.login_form['password'] = value
            form = CxUserLoginForm(data=self.login_form, instance=self.user)
            self.assertFalse(form.is_valid(), msg=f"Value: {value}")
