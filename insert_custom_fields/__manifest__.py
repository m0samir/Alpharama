# -*- coding: utf-8 -*-
# Author      : Nelson Omolo (<omolonlsn@gmail.com>)


{
    'name': 'Insert Custom Fields',
    'category': 'General',
    'author': 'Nelson Omolo',
    'description': """
                   Insert custom fields in core odoo modules
                 """,

    'depends': ['base', 'stock', 'mrp',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_production_lot_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_move_line_views.xml',
	'views/product_views.xml',
        'report/mrp_production_templates.xml',
        'views/vendor.xml',
        'views/invoice.xml',
    ],
    
    'installable': True,
    'auto_install': False,
}
