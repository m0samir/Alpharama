# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
{
    'name': 'Employee Age',
    'version': '12.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Human Resources',
    'description':
        """ 
        Odoo Apps add below functionality into odoo 
        
        1.Display Employee Age on Employee Form
        
    """,
    'summary': 'odoo Apps will help to add Employee Age on Employee screen', 
    'depends': ['hr'],
    'data': [
        'views/employee_view.xml'
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
