import datetime

from django.db import models

from apps.clients.models import Client
from apps.user_texts import MODEL_MSG
from apps.validators import validate_sap_id, validate_num_field, validate_int_field


class Product(models.Model):
    """Product model is consistent with SAP product model
    but contains only necessary data for quality control process. Extends product by
    specification data, related to quality control process.
    """
    product_sap_id = models.IntegerField(unique=True, validators=[validate_sap_id(), ])
    index = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Specification(models.Model):
    """Specification model is responsible for managing
    technical product data for quality control requirements.
    """
    CORES_PACKED_IN_CHOICES = list(zip(['Horizontal', 'Vertical', 'On_carton'], MODEL_MSG['cores_packed_in']))
    BOOLEAN_CHOICES = list(zip(["Y", "N"], MODEL_MSG['boolean_choices']))

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True, related_name="specification"
    )
    internal_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    external_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    wall_thickness_target = models.FloatField(validators=[validate_num_field(), ])
    wall_thickness_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    wall_thickness_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    length_target = models.FloatField(validators=[validate_num_field(), ])
    length_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    length_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    flat_crush_resistance_target = models.IntegerField(validators=[validate_int_field(), ])
    flat_crush_resistance_tolerance_top = models.IntegerField(validators=[validate_int_field(), ])
    flat_crush_resistance_tolerance_bottom = models.IntegerField(validators=[validate_int_field(), ])

    moisture_content_target = models.IntegerField(validators=[validate_int_field(), ])
    moisture_content_tolerance_top = models.IntegerField(validators=[validate_int_field(), ])
    moisture_content_tolerance_bottom = models.IntegerField(validators=[validate_int_field(), ])

    colour = models.CharField(max_length=100, blank=True)
    finish = models.CharField(max_length=100, blank=True)

    maximum_height_of_pallet = models.FloatField(validators=[validate_num_field(), ])
    pallet_protected_with_paper_edges = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                         default=BOOLEAN_CHOICES[0])
    pallet_wrapped_with_stretch_film = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                        default=BOOLEAN_CHOICES[0])
    cores_packed_in = models.CharField(max_length=20, choices=CORES_PACKED_IN_CHOICES,
                                       default=CORES_PACKED_IN_CHOICES[0][0])
    quantity_on_the_pallet = models.IntegerField(validators=[validate_int_field(), ])
    remarks = models.TextField()

    def __str__(self):
        return f"Specification of product: {self.product.description}"


class SpecificationIssued(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='issued_specifications',
                               to_field='client_sap_id')
    date_of_issue = models.DateField(default=datetime.date.today)

    CORES_PACKED_IN_CHOICES = list(zip(['Horizontal', 'Vertical', 'On_carton'], MODEL_MSG['cores_packed_in']))
    BOOLEAN_CHOICES = list(zip(["Y", "N"], MODEL_MSG['boolean_choices']))

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="issued_specifications",
                                to_field='product_sap_id')
    internal_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    internal_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    external_diameter_target = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    external_diameter_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    wall_thickness_target = models.FloatField(validators=[validate_num_field(), ])
    wall_thickness_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    wall_thickness_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    length_target = models.FloatField(validators=[validate_num_field(), ])
    length_tolerance_top = models.FloatField(validators=[validate_num_field(), ])
    length_tolerance_bottom = models.FloatField(validators=[validate_num_field(), ])

    flat_crush_resistance_target = models.IntegerField(validators=[validate_int_field(), ])
    flat_crush_resistance_tolerance_top = models.IntegerField(validators=[validate_int_field(), ])
    flat_crush_resistance_tolerance_bottom = models.IntegerField(validators=[validate_int_field(), ])

    moisture_content_target = models.IntegerField(validators=[validate_int_field(), ])
    moisture_content_tolerance_top = models.IntegerField(validators=[validate_int_field(), ])
    moisture_content_tolerance_bottom = models.IntegerField(validators=[validate_int_field(), ])

    colour = models.CharField(max_length=100, blank=True)
    finish = models.CharField(max_length=100, blank=True)

    maximum_height_of_pallet = models.FloatField(validators=[validate_num_field(), ])
    pallet_protected_with_paper_edges = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                         default=BOOLEAN_CHOICES[0])
    pallet_wrapped_with_stretch_film = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                        default=BOOLEAN_CHOICES[0])
    cores_packed_in = models.CharField(max_length=20, choices=CORES_PACKED_IN_CHOICES,
                                       default=CORES_PACKED_IN_CHOICES[0][0])
    quantity_on_the_pallet = models.IntegerField(validators=[validate_int_field(), ])
    remarks = models.TextField()

    def __str__(self):
        return f"Issued specification of product: {self.product.description} for client {self.client.client_name}"
