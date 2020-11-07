from django.contrib import auth
from django.core import mail

from django.test import TestCase, Client as ViewClient

from . import PASSWORD
from .factories import CxUserFactory
from ..forms import CxUserLoginForm, CxUserPasswordChangeForm, CxUserEmailChangeForm
from ...unittest_utils import assert_response_get, assert_response_post


class UsersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view_client = ViewClient()
        cls.user = CxUserFactory.create()
        cls.form_data = {'username': cls.user.username, 'password': PASSWORD}

    def test_login_get(self):
        response = assert_response_get(test_case=self, url_name='users:user_login',
                                       exp_status_code=200, exp_template='login_form.html')
        self.assertTrue(isinstance(response.context['form'], CxUserLoginForm))

    def test_login_post(self):
        assert_response_post(test_case=self, url_name='users:user_login',
                             exp_status_code=302, data=self.form_data)
        user = auth.get_user(self.view_client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        assert_response_get(test_case=self, url_name='users:user_logout',
                            exp_status_code=302)
        user = auth.get_user(self.view_client)
        self.assertFalse(user.is_authenticated)

    def test_reset_password_get(self):
        response = assert_response_get(test_case=self, url_name='users:password_reset',
                                       exp_status_code=200)
        self.assertTrue(isinstance(response.context.get('user_form'), CxUserLoginForm))

    def test_reset_password_post(self):
        assert_response_post(test_case=self, url_name='users:password_reset',
                             exp_status_code=302, data={'username': self.user.username})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'admin@example.com')
        self.assertEqual(mail.outbox[0].to[0], self.user.email)

    def test_user_password_reset_done(self):
        response = assert_response_get(test_case=self, url_name='users:password_reset_done',
                                       exp_status_code=200, id=self.user.id)
        self.assertIsNotNone(response.context.get('domain'))

    def test_user_profile(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_get(test_case=self, url_name='users:user_profile', exp_status_code=200)

    def test_user_password_change_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='users:password_change', exp_status_code=200)
        self.assertTrue(isinstance(response.context.get('form'), CxUserPasswordChangeForm))

    def test_user_password_change_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        new_password = 'utest122'
        assert_response_post(test_case=self, url_name='users:password_change',
                             exp_status_code=302, data={'old_password': PASSWORD, 'new_password1': new_password,
                                                        'new_password2': new_password})
        user = auth.get_user(self.view_client)
        self.assertTrue(user.check_password(new_password))

    def test_user_email_change_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='users:email_change', exp_status_code=200)
        self.assertTrue(isinstance(response.context.get('form'), CxUserEmailChangeForm))

    def test_user_email_change_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        new_email = 'test2@test.com'
        assert_response_post(test_case=self, url_name='users:email_change',
                             exp_status_code=302, data={'email': new_email})
        user = auth.get_user(self.view_client)
        self.assertEqual(user.email, new_email)
