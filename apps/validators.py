from django.core.validators import RegexValidator


REGEXPS = {
    'client': {'client_sap_id': '^([0-9]{6})$'}
}


def validate_sap_id():
    return RegexValidator(regex=REGEXPS['client']['client_sap_id'],
                          message="SAP id klienta musi być numerem składającym się z 6 cyfr",
                          code='invalid sap id')
