# -*- coding: utf-8 -*-
{
    'name': "Hr Work Entries For Kenya",
    'license': 'OPL-1',

    'summary': """
        Hr Work Entries For Kenya""",

    'description': """
        Hr Work Entries For Kenya
    """,
    'author': "Thilak",
    'website': "",
    'category': 'Human Resources',

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
