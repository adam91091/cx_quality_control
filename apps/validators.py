from django.core.validators import RegexValidator


def validate_sap_id():
    return RegexValidator(regex='^([0-9]{6})$',
                          message="SAP id klienta musi być numerem składającym się z 6 cyfr",
                          code='invalid sap id')
