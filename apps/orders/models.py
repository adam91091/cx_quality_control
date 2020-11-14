import datetime
from django.db import models
from django.db.models import Min, Max

from apps.clients.models import Client
from apps.products.models import Product
from apps.validators import validate_num_field, validate_int_field, validate_order_sap_id


class Order(models.Model):
    STATUS_CHOICES = [('Started', 'Otwarty'),
                      ('Open', 'W trakcie'),
                      ('Done', 'Zakończony')]
    order_sap_id = models.IntegerField(unique=True, validators=[validate_order_sap_id(), ], null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', to_field='client_sap_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', to_field='product_sap_id')
    date_of_production = models.DateField(default=datetime.date.today)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], max_length=30)
    quantity = models.IntegerField(validators=[validate_int_field(), ], null=True, blank=True)
    # tube sizing information
    internal_diameter_reference = models.FloatField(validators=[validate_num_field(), ], null=True, blank=True)
    external_diameter_reference = models.FloatField(validators=[validate_num_field(), ], null=True, blank=True)
    length = models.FloatField(validators=[validate_num_field(), ], null=True, blank=True)

    def __str__(self):
        return f"Zlecenie produkcyjne. Nr partii: {self.order_sap_id} " \
               f"Kod produktu: {self.product.product_sap_id} Klient: {self.client}"

    @staticmethod
    def get_date_of_production(value):
        dates = {'min': Order.objects.aggregate(Min('date_of_production'))['date_of_production__min'],
                 'max': Order.objects.aggregate(Max('date_of_production'))['date_of_production__max'],
                 'today': datetime.date.today()}
        return dates.get(value).strftime('%Y-%m-%d')


class MeasurementReport(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='measurement_report')
    author = models.CharField(max_length=100)
    date_of_control = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Raport pomiarowy do zlecenia produkcyjnego nr {self.order.order_sap_id}"


class Measurement(models.Model):
    measurement_report = models.ForeignKey(MeasurementReport, on_delete=models.CASCADE, related_name='measurements')
    pallet_number = models.IntegerField(validators=[validate_int_field(), ])

    internal_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    external_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    length_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    length_target = models.FloatField(validators=[validate_num_field(), ])
    length_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    flat_crush_resistance_target = models.IntegerField(validators=[validate_int_field(), ], null=True, blank=True)
    moisture_content_target = models.IntegerField(validators=[validate_int_field(), ], null=True, blank=True)
    weight = models.IntegerField(validators=[validate_int_field(), ], null=True, blank=True)

    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pomiar palety nr {self.pallet_number}. " \
               f"Raport pomiarowy zlecenia produkcyjnego nr: {self.measurement_report.order.order_sap_id}"
