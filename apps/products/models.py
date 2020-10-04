from django.db import models
from django.db.models import Field, Transform

from apps.validators import validate_sap_id, validate_num_field, validate_int_field


@Field.register_lookup
class CharValue(Transform):
    lookup_name = 'char'
    bilateral = False

    def as_sql(self, compiler, connection, function=None, template=None, arg_joiner=None, **extra_context):
        sql, params = compiler.compile(self.lhs)
        sql = 'CAST(%s AS CHAR)' % sql
        return sql, params


class Product(models.Model):
    product_sap_id = models.IntegerField(unique=True, validators=[validate_sap_id(), ])
    index = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Specification(models.Model):
    CORES_PACKED_IN_CHOICES = [('Horizontal', 'w pozycji pionowej'),
                               ('Vertical', 'w pozycji poziomej'),
                               ('On_carton', 'na kartonach')]
    BOOLEAN_CHOICES = [("Y", 'Tak'), ("N", 'Nie')]

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
    quantity_on_the_pallet = models.IntegerField(validators=[validate_int_field(), ])
    pallet_protected_with_paper_edges = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                         default=BOOLEAN_CHOICES[0])
    pallet_wrapped_with_stretch_film = models.CharField(max_length=10, choices=BOOLEAN_CHOICES,
                                                        default=BOOLEAN_CHOICES[0])
    cores_packed_in = models.CharField(max_length=20, choices=CORES_PACKED_IN_CHOICES,
                                       default=CORES_PACKED_IN_CHOICES[0][0],
                                       )
    remarks = models.TextField()

    def __str__(self):
        return "Specyfikacja produktu: {}".format(self.product.description)
