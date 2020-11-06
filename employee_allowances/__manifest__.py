# -*- coding: utf-8 -*-
{
    'name': "Allowances | Deductions Allocation",

    'summary': """
        Employee Allowances""",

    'description': """
        Fine Employees, Allocate bonuses and commissions to employees.
        This also include all other types of deductions and allowances.
        Manage Employee Overtime allowances.
        Send email notification to an employee's manager 14 Days prior to the employee's contract expiry.
        Includes the P9 report for employees
        Modify the Netpay and Payroll Summary reports for employee's payslips
    """,

    'author': "Eric Waweru",
    'website': "http://www.yourcompany.com",

    'category': 'Extra Tools',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'hr_ke', 'product_combo_pack', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',

        'wizards/fine_wizard.xml',
        'wizards/overtime_wizard.xml',
        'wizards/bonus_wizard.xml',
        'wizards/p9.xml',

        'views/overtime.xml',
        'views/deductions.xml',
        'views/views.xml',

        'reports/misc.xml',
        'reports/templates.xml',
        'reports/p9.xml',
        'reports/payslip.xml',
        'reports/delivery_slip.xml',
        'reports/report.xml',
    ],

}
