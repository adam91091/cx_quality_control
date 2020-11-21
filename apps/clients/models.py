from django.db import models

from apps.validators import validate_sap_id


class Client(models.Model):
    """Client model is consistent with SAP client model
    but contains only necessary data for quality control process.
    """
    client_sap_id = models.IntegerField(unique=True, validators=[validate_sap_id(), ])
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return self.client_name
