# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Purchase Return',
    'version' : '1.1',
    'summary': 'Purchase Return of Selected Products',
    'sequence': 16,
    'description': """Purchase Return of Selected Products""",
    'category': 'Extension of Kenya Purchase',
    'website': '',
    'depends' : ['base', 'purchase'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
