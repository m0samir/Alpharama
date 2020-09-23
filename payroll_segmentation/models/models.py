# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError, AccessError
from odoo import api, fields, models, _
import pdb


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    payroll_segmentation = fields.Selection([
        ('Junior', "Junior"),
        ('Senior', "Senior")], default=False, required=True)


class PieceRateLines(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_payroll_segmentation(self):
        # pdb.set_trace()
        if self.employee_id and self.employee_id.payroll_segmentation == "Junior" and \
                self.env.user.has_group('payroll_segmentation.group_payroll_junior'):
            return
        elif self.employee_id and self.employee_id.payroll_segmentation == "Senior" and \
                self.env.user.has_group('payroll_segmentation.group_payroll_senior'):
            return
        elif self.employee_id:
            raise AccessError(_("You do not have access, to generate payroll for this employee(s)."))


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    @api.multi
    def compute_sheet(self):
        for rec in self.employee_ids:
            # pdb.set_trace()
            if rec.name and rec.payroll_segmentation == "Junior" and \
                    self.env.user.has_group('payroll_segmentation.group_payroll_junior'):
                pass
            elif rec.name and rec.payroll_segmentation == "Senior" and \
                    self.env.user.has_group('payroll_segmentation.group_payroll_senior'):
                pass
            elif rec.name:
                raise AccessError(_("You do not have access, to generate payslip for this employee(s)."))

        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            payslip_run = self.env['hr.payslip.run'].create({
                'name': from_date.strftime('%B %Y'),
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        if not self.employee_ids:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))

        payslips = self.env['hr.payslip']
        Payslip = self.env['hr.payslip']

        contracts = self.employee_ids._get_contracts(payslip_run.date_start, payslip_run.date_end,
                                                     states=['open', 'close'])
        contracts._generate_work_entries(payslip_run.date_start, payslip_run.date_end)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', self.employee_ids.ids),
        ])
        self._check_undefined_slots(work_entries, payslip_run)

        validated = work_entries.action_validate()
        if not validated:
            raise UserError(_("Some work entries could not be validated."))

        default_values = Payslip.default_get(Payslip.fields_get())
        for contract in contracts:
            values = dict(default_values, **{
                'employee_id': contract.employee_id.id,
                'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': self.structure_id.id or contract.structure_type_id.default_struct_id.id,
            })
            payslip = self.env['hr.payslip'].new(values)
            payslip._onchange_employee()
            values = payslip._convert_to_write(payslip._cache)
            payslips += Payslip.create(values)
        payslips.compute_sheet()
        payslip_run.state = 'verify'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.run',
            'views': [[False, 'form']],
            'res_id': payslip_run.id,
        }
