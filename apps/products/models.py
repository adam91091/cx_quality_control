from django.db import models


class Product(models.Model):
    product_sap_id = models.IntegerField(unique=True)
    index = models.CharField(max_length=30)
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
    internal_diameter_target = models.FloatField()
    internal_diameter_tolerance_top = models.FloatField()
    internal_diameter_tolerance_bottom = models.FloatField()

    external_diameter_target = models.FloatField()
    external_diameter_tolerance_top = models.FloatField()
    external_diameter_tolerance_bottom = models.FloatField()

    wall_thickness_target = models.FloatField()
    wall_thickness_tolerance_top = models.FloatField()
    wall_thickness_tolerance_bottom = models.FloatField()

    length_target = models.FloatField()
    length_tolerance_top = models.FloatField()
    length_tolerance_bottom = models.FloatField()

    flat_crush_resistance_target = models.IntegerField()
    flat_crush_resistance_tolerance_top = models.IntegerField()
    flat_crush_resistance_tolerance_bottom = models.IntegerField()

    moisture_content_target = models.IntegerField()
    moisture_content_tolerance_top = models.IntegerField()
    moisture_content_tolerance_bottom = models.IntegerField()

    colour = models.CharField(max_length=100, blank=True)
    finish = models.CharField(max_length=100, blank=True)

    maximum_height_of_pallet = models.FloatField()
    quantity_on_the_pallet = models.IntegerField()
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