from django.db import models
from django.db.models import Field, Transform

from apps.validators import validate_sap_id


@Field.register_lookup
class CharValue(Transform):
    lookup_name = 'char'
    bilateral = False

    def as_sql(self, compiler, connection, function=None, template=None, arg_joiner=None, **extra_context):
        sql, params = compiler.compile(self.lhs)
        sql = 'CAST(%s AS CHAR)' % sql
        return sql, params


class Client(models.Model):
    client_sap_id = models.IntegerField(unique=True, validators=[validate_sap_id(), ])
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return self.client_name
