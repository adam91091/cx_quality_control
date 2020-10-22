import datetime
from apps.validators import REGEXPS

# Widget attrs helper dicts
BASIC_STYLE = {'class': 'form-control'}

BASIC_REQ_STYLE = {'class': 'form-control', 'required': 'true'}

BASIC_NO_HINTS_STYLE = {'class': 'form-control no-hints'}

NUM_STYLE_NO_REQ = {'class': 'form-control',
                    'pattern': REGEXPS['common']['num_field'], }

NUM_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['num_field'], }

INT_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['int_field'], }

SAP_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['sap_id'], }

ORDER_SAP_STYLE = {'class': 'form-control',
                   'required': 'true',
                   'pattern': REGEXPS['order']['order_sap_id']}

DATE_STYLE = {'class': 'form-control', }

INPUT_MEASUREMENT_FORM_STYLE_50px = {'style': 'height: 50px; border-radius: 0;'}
INPUT_MEASUREMENT_FORM_STYLE_70px = {'style': 'height: 70px; border-radius: 0;'}
INPUT_MEASUREMENT_FORM_STYLE_71px = {'style': 'height: 71px; border-radius: 0;'}
