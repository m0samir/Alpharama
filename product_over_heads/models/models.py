from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from odoo import api, fields, models, _


class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'
    
    department = fields.Many2one('hr.department', string="Department")
    boolean = fields.Boolean(default=False, compute='update_department')
    
    def update_department(self):
        if not self.boolean and self.employee_id:
            self.boolean = True
            self.department = self.employee_id.department_id    