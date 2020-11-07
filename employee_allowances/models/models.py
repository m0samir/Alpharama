from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
import json


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    fine_amount = fields.Float(string='Amount')
    deduction_id = fields.Many2one(
        'ke.deductions.type', string='Deduction Type')
    rule_id = fields.Many2one(
        related='deduction_id.rule_id', string="Salary Rule")
    overtime_hours = fields.Float(string='Overtime Hours')
    contract_id = fields.Many2one('hr.contract', string='Contract')

    bank_name = fields.Char(string='Bank')
    bank_branch = fields.Char(string='Bank Branch')
    employee_bank_account = fields.Char(string='Employee\'s Account Number')
    branch_code = fields.Char(string='Bank Branch Code')


class HrContract(models.Model):
    _inherit = 'hr.contract'

    cash_allowance_id = fields.Many2one(
        'ke.cash.allowances.type', string='Allowance Type')
    allowance_amount = fields.Float(string='Amount')

    rule_id = fields.Many2one(string='Salary Rule',
                              related='cash_allowance_id.rule_id')

    @api.model
    def contract_expiry(self):
        expiry_date = datetime.now().date() + timedelta(days=14)

        for rec in self.search([('state', 'in', ['open'])]):
            if rec.date_end and rec.employee_id.parent_id:
                if expiry_date == rec.date_end:

                    mail_content = "Hello  " + rec.employee_id.parent_id.name + ",<br>Your employee " + \
                        rec.employee_id.name + \
                        "contract is going to expire in 14 Days. Please review it and possibly renew."

                    main_content = {
                        'subject': _('%s Contract Expiry') % (rec.employee_id.name),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': rec.employee_id.parent_id.work_email,
                    }
                    self.env['mail.mail'].create(main_content).send()

                    rec.update({'state': 'pending'})


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        # execute original code
        res = super().action_payslip_done()
        for record in self:
            deductions = self.env['ke.deductions'].search(
                [('employee_id', '=', record.employee_id.id)])

            allowances = self.env['ke.cash_allowances'].search(
                [('contract_id', '=', record.contract_id.id)])

        for rec in deductions:
            deduction = self.env['ke.deductions.type'].search(
                [('id', '=', rec.deduction_id.id)]).mapped('recurring_deduction')
            if deduction[0] == False:
                rec.unlink()

        for rec in allowances:
            allowance = self.env['ke.cash.allowances.type'].search(
                [('id', '=', rec.cash_allowance_id.id)]).mapped('recurring_allowance')
            if allowance[0] == False:
                rec.unlink()

        return self.write({'state': 'done'})


class KeCashAllowanceType(models.Model):
    _inherit = 'ke.cash.allowances.type'

    recurring_allowance = fields.Boolean(
        string='Recurring Allowance', help='This type of allowance is recurrent every month.')


class KeDeductionType(models.Model):
    _inherit = 'ke.deductions.type'

    recurring_deduction = fields.Boolean(
        string='Recurring Deduction', help='This type of deduction is recurrent every month.')


class KeBatchDeduction(models.Model):
    _name = 'ke.batch.deduction'
    _description = 'Batch Deduction Allocation'

    def action_confirm_deductions(self):
        if len(self.deduction_ids) == 0:
            raise ValidationError(
                'You must have atleast one employee selected to continue with this operation!')
        else:
            for rec in self.deduction_ids:
                vals = {
                    'deduction_id': rec.deduction_type_id.id,
                    'computation': 'fixed',
                    'fixed': rec.amount,
                    'employee_id': rec.employee_id.id,
                }
                self.env['ke.deductions'].sudo().create(vals)
            self.write({'state': 'confirm'})

    name = fields.Char(string='Brief Title', required=True)
    note = fields.Text(string='Note')
    date = fields.Date(string='Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    deduction_ids = fields.One2many(
        'ke.batch.deduction.ids', 'deduction_id', string='Deduction Ids')
    details = fields.Html(string='Details')


class KeBatchDeductionIds(models.Model):
    _name = 'ke.batch.deduction.ids'
    _description = 'Batch Deduction Ids'

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True)
    deduction_type_id = fields.Many2one(
        'ke.deductions.type', string='Deduction Type', required=True)
    rule_id = fields.Many2one(
        related='deduction_type_id.rule_id', string="Salary Rule")
    amount = fields.Float(string='Amount')
    deduction_id = fields.Many2one('ke.batch.deduction', string='Deduction Id')


class KEPayrollSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    employer_bank_account = fields.Char(
        'Employer Bank Account.', required=False)
