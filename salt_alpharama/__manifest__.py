{
    'name': 'Salt Solution for Alpharama',
    'version': '12.0.1.0.0',
    "author": "Thilak",
    'license': 'AGPL-3',
    'category': 'Stock',
    'website': '',
	'depends': ['stock_landed_costs'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
        'security/account_security.xml',
    ],

    'installable': True,
	'auto_install': False,
}

