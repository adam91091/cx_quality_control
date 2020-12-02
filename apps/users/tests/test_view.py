from django.contrib import auth

from django.test import TestCase, Client as ViewClient

from . import PASSWORD
from .factories import CxUserFactory
from ..forms import CxUserPasswordChangeForm, CxUserAuthenticationForm
from ...unittest_helpers import assert_response_get, assert_response_post


class UsersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view_client = ViewClient()
        cls.user = CxUserFactory.create()
        cls.form_data = {'username': cls.user.username, 'password': PASSWORD}

    def test_login_get(self):
        response = assert_response_get(test_case=self, url_name='users:user-login',
                                       exp_status_code=200, exp_template='login_form.html')
        self.assertTrue(isinstance(response.context['form'], CxUserAuthenticationForm))

    def test_login_post(self):
        assert_response_post(test_case=self, url_name='users:user-login',
                             exp_status_code=302, data=self.form_data)
        user = auth.get_user(self.view_client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        assert_response_get(test_case=self, url_name='users:user-logout',
                            exp_status_code=302)
        user = auth.get_user(self.view_client)
        self.assertFalse(user.is_authenticated)

    def test_user_profile(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_get(test_case=self, url_name='users:user-profile', exp_status_code=200)

    def test_user_password_change_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='users:password-change', exp_status_code=200)
        self.assertTrue(isinstance(response.context.get('form'), CxUserPasswordChangeForm))

    def test_user_password_change_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        new_password = 'utest122'
        assert_response_post(test_case=self, url_name='users:password-change',
                             exp_status_code=302, data={'old_password': PASSWORD, 'new_password1': new_password,
                                                        'new_password2': new_password})
        user = auth.get_user(self.view_client)
        self.assertTrue(user.check_password(new_password))
