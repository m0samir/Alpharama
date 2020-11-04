# -*- coding: utf-8 -*-
{
    'name': "Payroll and HR System For Kenya",
    'license': 'OPL-1',
    'support': 'support@optima.co.ke',

    'summary': """
        Automated Payroll and HR system customized for Kenya, with KRA reports and automated Tax Returns """,

    'description': """
        In this module, we are adding Kenya specific HR details and requirements for processing payroll. NSSF, NHIF, Next Of Kin, PAYE, HELB and others
    """,
    'images': ['static/description/hr.png'],
    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",
    'price': 351,
    'currency': 'EUR',
    'category': 'Human Resources',
    'version': '0.6',

    # any module necessary for this one to work correctly
    'depends': ['hr_work_entry'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
