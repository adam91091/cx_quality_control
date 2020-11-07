from django.core.validators import RegexValidator

REGEXPS = {
    'common': {'sap_id': r'^([0-9]{7})$',
               'num_field': r'^([0-9]*|[0-9]*\.\d+)$',
               'int_field': r'^[0-9]*$', },
    'order': {'order_sap_id': r'^([0-9]{8})$', },
    'user': {'username': r'^([a-z]{5})$',
             'password': r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', }
}


def validate_sap_id():
    return RegexValidator(regex=REGEXPS['common']['sap_id'],
                          message="Numer SAP powinien składać się z dokładnie 7 cyfr",
                          code='invalid sap id')


def validate_order_sap_id():
    return RegexValidator(regex=REGEXPS['order']['order_sap_id'], message="Numer partii powinien składać się z "
                                                                          "dokładnie 8 cyfr", code='invalid sap id')


def validate_num_field():
    return RegexValidator(regex=REGEXPS['common']['num_field'],
                          message="Pole float powinno zawierać liczbę całkowitą bądź zmiennoprzecinkową")


def validate_int_field():
    return RegexValidator(regex=REGEXPS['common']['int_field'],
                          message="Pole integer powinno zawierać liczbę całkowitą")


def validate_username():
    return RegexValidator(regex=REGEXPS['user']['username'],
                          message="Login powinien składać się z dokładnie pięciu małych liter")
