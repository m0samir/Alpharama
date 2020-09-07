# -*- coding: utf-8 -*-
{
    'name': "Bom Report",

    'summary': """
        Print BOM and Lot reports""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Eric Waweru",
    'website': "http://www.yourcompany.com",

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': ['mrp'],

    'data': [
        'wizards/wizard.xml',
        'reports/report.xml',
        'reports/templates.xml',
        'reports/multiple_yields.xml',
        'reports/mo_report.xml',

        'views/views.xml',
    ],
}
