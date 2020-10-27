import factory

from apps.users.models import CxUser
from apps.users.tests import PASSWORD


class CxUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = CxUser

    username = 'utest'
    email = 'utest@test.com'
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)
