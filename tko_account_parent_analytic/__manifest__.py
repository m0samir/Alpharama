# -*- coding: utf-8 -*-

{
    'name': 'Parent Analytic Account',
    'summary': '',
    'description': 'Creates parent child relationship in analytic accounts',
    'author': 'TKO',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'website': 'http://tko.tko-br.com',
    'version': '10.0.0.0.0',
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': ['analytic',
                'account'], # depending only to create menu
    'external_dependencies': {
                                'python': [],
                                'bin': [],
                                },
    'init_xml': [],
    'update_xml': [],
    'css': [],
    'demo_xml': [],
    'test': [],
    'data': [
        'views/account_analytic_account_view.xml',
        'wizard/open_analytic_chart.xml',
    ],
}
