import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

class HREmployeeExtend(models.Model):
    _inherit = 'hr.employee'
    legal_leaves_count = fields.Float('Number of Legal Leaves', compute='_compute_leaves_count')

    @api.multi
    def _compute_leaves_count(self):
        all_leaves = self.env['hr.leave.report'].read_group([
            ('employee_id', 'in', self.ids),
            ('holiday_status_id.allocation_type', '!=', 'no'),
            ('state', '=', 'validate')
        ], fields=['number_of_days', 'employee_id'], groupby=['employee_id'])
        mapping = dict([(leave['employee_id'][0], leave['number_of_days']) for leave in all_leaves])
        for employee in self:
            employee.leaves_count = float_round(mapping.get(employee.id, 0), precision_digits=2)