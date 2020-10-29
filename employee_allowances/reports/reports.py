from odoo import models, api


class P9Report(models.AbstractModel):
    _name = 'report.employee_allowances.employee_p9_report'
    _description = 'Employee P9 Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids[0])

        return {
            'docs': docs,
        }
