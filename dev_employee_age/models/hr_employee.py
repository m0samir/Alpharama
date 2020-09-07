# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from datetime import date, datetime


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    employee_age = fields.Char(string="Age")
    
    @api.onchange('birthday')
    def onchange_employee_birthday(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            self.employee_age = str(age)
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
