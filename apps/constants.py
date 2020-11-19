PRODUCT_SAP_DIGITS = 7
ORDER_SAP_DIGITS = 8
CLIENT_SAP_DIGITS = 7

FLOAT_DEFAULT = 1.0
INT_DEFAULT = 1

PAGINATION_LINKS_MAX_COUNT = 20
PAGINATION_OBJ_COUNT_PER_PAGE = 10

STRFTIME_STRING = '%Y-%m-%d 00:00:00'

VIEW_MSG = {'client': {'new_success': "Utworzono nowego klienta",
                       'new_error': "Nie utworzono nowego klienta. "
                                    "Wystąpiły następujące błędy formularza:",
                       'update_success': "Zaktualizowano dane klienta",
                       'update_error': "Nie zaktualizowano danych klienta. "
                                       "Wystąpiły następujące błędy formularza:",
                       'delete_success': "Klient został usunięty", },
            'product': {'new_success': "Utworzono nowy produkt",
                        'new_error': "Nie utworzono nowego produktu. "
                                     "Wystąpiły następujące błędy formularza:",
                        'update_success': "Zaktualizowano dane produktu",
                        'update_error': "Nie zaktualizowano danych produktu",
                        'delete_success': "Produkt został usunięty", },
            'order': {'new_success': "Utworzono nowe zlecenie produkcyjne",
                      'new_error': "Nie utworzono nowego zlecenia produkcyjnego. "
                                   "Wystąpiły następujące błędy formularza:",
                      'update_success': "Zaktualizowano dane zlecenia produkcyjnego",
                      'update_error': "Nie zaktualizowano danych zlecenia produkcyjnego. "
                                      "Wystąpiły następujące błędy formularza:",
                      'delete_success': "Zlecenie produkcyjne zostało usunięte", },
            'measurement_report': {'new_success': "Dodano raport pomiarowy",
                                   'new_error': "Raport pomiarowy nie został dodany. "
                                                "Wystąpiły następujące błędy formularza:",
                                   'update_success': "Zaktualizowano raport pomiarowy",
                                   'update_error': "Nie zaktualizowano raportu pomiarowego. "
                                                   "Wystąpiły następujące błędy formularza:",
                                   'close_success': "Pomiary zostały zakończone",
                                   },
            'user': {'login_success': 'Logowanie zakończyło się sukcesem',
                     'logout_success': 'Wylogowano z systemu',
                     'login_fail': 'Logowanie zakończone niepowodzeniem. Wystąpiły następujące błędy formularza:',
                     'inactive': "Użytkownik jest nieaktywny i został zablokowany w systemie",
                     'password_change_success': 'Hasło zostało zmienione',
                     'password_change_fail': "Hasło nie zostało zmienione. Wystąpiły następujące błędy formularza:",
                     'email_change_success': "Adres email został zmieniony",
                     'email_change_error': "Adres email nie został zmieniony. Wystąpiły następujące błędy formularza:",
                     }
            }
