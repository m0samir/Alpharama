# -*- coding: utf-8 -*-
{
    'name': "Product Over Heads",
    'license': 'OPL-1',

    'summary': """
        Product Over Heads """,

    'description': """
        Product Over Heads
    """,
    'author': "Thilak",
    'website': "",
    'category': 'Manufacturing',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

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
