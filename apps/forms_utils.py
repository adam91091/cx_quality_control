from apps.validators import REGEXPS

# Widget attrs helper dicts
BASIC_STYLE = {'class': 'form-control'}

BASIC_REQ_STYLE = {'class': 'form-control', 'required': 'true'}

BASIC_NO_HINTS_STYLE = {'class': 'form-control no-hints'}

NUM_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['num_field'], }

INT_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['int_field'], }

SAP_STYLE = {'class': 'form-control',
             'required': 'true',
             'pattern': REGEXPS['common']['sap_id'], }
