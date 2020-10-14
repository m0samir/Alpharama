# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
<<<<<<< HEAD
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
=======
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
>>>>>>> 6559eaf031b8eb1c6a34277b717674ce81ff44ca
#
##############################################################################

from odoo import models, fields, api, tools

<<<<<<< HEAD

=======
>>>>>>> 6559eaf031b8eb1c6a34277b717674ce81ff44ca
class InstallmentAnalyticLineView(models.Model):
    _name = 'employee.loan.report.view'
    _table = 'employee_loan_report_view'
    _description = "Employee Loan View"
    _auto = False
    _rec_name = 'date'
<<<<<<< HEAD

    name = fields.Char('Loan')
    employee_id = fields.Many2one('hr.employee', string='Employee')
=======
    
    
    name = fields.Char('Loan')
    employee_id = fields.Many2one('hr.employee',string='Employee')
>>>>>>> 6559eaf031b8eb1c6a34277b717674ce81ff44ca
    date = fields.Date('Date')
    department_id = fields.Many2one('hr.department', string='Department')
    manager_id = fields.Many2one('hr.employee', string='Manager')
    job_id = fields.Many2one('hr.job', string='Job Position')
    loan_type_id = fields.Many2one('employee.loan.type', string='Loan Type')
    term = fields.Integer('Term')
    interest_rate = fields.Float('Interest Rate')
<<<<<<< HEAD
    n_paid_amount = fields.Float('Paid Amount')
    n_interest_amount = fields.Float('Interest Amount')
    n_extra_in_amount = fields.Float('Extra Interest Amount')
    n_remaing_amount = fields.Float('Remaing Amount')

    loan_amount = fields.Float('Loan Amount')
    state = fields.Selection([('draft', 'Draft'),
                              ('request', 'Submit Request'),
                              ('dep_approval', 'Department Approval'),
                              ('hr_approval', 'HR Approval'),
                              ('paid', 'Paid'),
                              ('done', 'Done'),
                              ('close', 'Close'),
                              ('reject', 'Reject'),
                              ('cancel', 'Cancel')], string='State')

    # @api.model_cr

=======
    n_paid_amount= fields.Float('Paid Amount')
    n_interest_amount = fields.Float('Interest Amount')
    n_extra_in_amount = fields.Float('Extra Interest Amount')
    n_remaing_amount = fields.Float('Remaing Amount')
    
    loan_amount = fields.Float('Loan Amount')
    state = fields.Selection([('draft','Draft'),
                                ('request','Submit Request'),
                                ('dep_approval','Department Approval'),
                                ('hr_approval','HR Approval'),
                                ('paid','Paid'),
                                ('done','Done'),
                                ('close', 'Close'),
                                ('reject','Reject'),
                                ('cancel','Cancel')], string='State')
    
    
    
>>>>>>> 6559eaf031b8eb1c6a34277b717674ce81ff44ca
    def init(self):
        tools.drop_view_if_exists(self._cr, 'employee_loan_report_view')
        self._cr.execute("""
          CREATE OR REPLACE VIEW employee_loan_report_view AS
          SELECT el.id,
                 el.name,
                 el.employee_id,
                 el.date,
                 el.department_id,
                 el.manager_id,
                 el.job_id,
                 el.loan_type_id,
                 el.term,
                 el.interest_rate,
                 el.state,
                 el.loan_amount,
                 el.n_interest_amount,
                 el.n_paid_amount,
                 el.n_extra_in_amount,
                 el.n_remaing_amount FROM employee_loan el where el.state in ('close','done'); """)


<<<<<<< HEAD
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:            
>>>>>>> 6559eaf031b8eb1c6a34277b717674ce81ff44ca
