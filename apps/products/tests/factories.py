import factory

from apps.constants import PRODUCT_SAP_DIGITS, FLOAT_DEFAULT, INT_DEFAULT
from apps.products.models import Product, Specification


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    product_sap_id = factory.Sequence(lambda n: 10 ** (PRODUCT_SAP_DIGITS - 1) + n)
    index = factory.Sequence(lambda n: f"test_index_{n}")
    description = factory.Sequence(lambda n: f"test_description_{n}")


class SpecificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Specification

    product = factory.SubFactory(ProductFactory)
    internal_diameter_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    internal_diameter_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    internal_diameter_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    external_diameter_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    external_diameter_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    external_diameter_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    wall_thickness_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    wall_thickness_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    wall_thickness_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    length_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    length_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    length_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    flat_crush_resistance_target = factory.Sequence(lambda n: INT_DEFAULT + n)
    flat_crush_resistance_tolerance_top = factory.Sequence(lambda n: INT_DEFAULT + n)
    flat_crush_resistance_tolerance_bottom = factory.Sequence(lambda n: INT_DEFAULT + n)

    moisture_content_target = factory.Sequence(lambda n: INT_DEFAULT + n)
    moisture_content_tolerance_top = factory.Sequence(lambda n: INT_DEFAULT + n)
    moisture_content_tolerance_bottom = factory.Sequence(lambda n: INT_DEFAULT + n)

    colour = factory.Sequence(lambda n: f"test_colour_{n}")
    finish = factory.Sequence(lambda n: f"test_finish_{n}")

    maximum_height_of_pallet = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    quantity_on_the_pallet = factory.Sequence(lambda n: INT_DEFAULT + n)
    pallet_protected_with_paper_edges = 'Y'
    pallet_wrapped_with_stretch_film = 'N'
    cores_packed_in = 'Vertical'
    remarks = factory.Sequence(lambda n: f"test_remarks_{n}")
