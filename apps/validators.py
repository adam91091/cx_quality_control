from django.core.validators import RegexValidator

REGEXPS = {
    'common': {'sap_id': '^([0-9]{6})$',
               'num_field': '^([0-9]*|[0-9]*\.\d+)$',
               'int_field': '^[0-9]*$', },
}


def validate_sap_id():
    return RegexValidator(regex=REGEXPS['common']['sap_id'],
                          message="Numer SAP powinien składać się z dokładnie 6 cyfr",
                          code='invalid sap id')


def validate_num_field():
    return RegexValidator(regex=REGEXPS['common']['num_field'],
                          message="Pole float powinno zawierać liczbę całkowitą bądź zmiennoprzecinkową")


def validate_int_field():
    return RegexValidator(regex=REGEXPS['common']['int_field'],
                          message="Pole integer powinno zawierać liczbę całkowitą")
