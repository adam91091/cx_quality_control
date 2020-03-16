from django.db import models


class Client(models.Model):
    client_sap_id = models.IntegerField(unique=True)
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return self.client_name
