from odoo import models, api


class AlpharamaPayslip(models.AbstractModel):
    _name = 'report.employee_allowances.alpharama_payslip'
    _description = 'Alpharama Payslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids)
        data = []
        for doc in docs:
            val = {
                'name': doc.employee_id.name,
                'department': doc.employee_id.department_id.name,
                'payroll': doc.employee_id.payroll_no,
                'kampuni': {
                    'name': doc.company_id.name,
                    'street': doc.company_id.street,
                    'city': f'{doc.company_id.city} {doc.company_id.zip}',
                    'country': doc.company_id.country_id.name,
                },
                'basic': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule10').id), ('slip_id', '=', doc.id)], limit=1).total or 0.0,
                'house': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule17').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'gross': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule30').id), ('slip_id', '=', doc.id)], limit=1).total or 0.0,
                'paye': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule105').id), ('slip_id', '=', doc.id)], limit=1).total or 0.0,
                'nssf': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule55').id), ('slip_id', '=', doc.id)], limit=1).total or 0.0,
                'nhif': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule106').id), ('slip_id', '=', doc.id)], limit=1).total or 0.0,
                'advance': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule108').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'contribution': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule65').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'taxable_income': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule85').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'taxable_charge': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule90').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'relief': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule95').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
                'net_pay': doc.line_ids.search([('salary_rule_id', '=', self.env.ref(
                    'hr_ke.ke_rule120').id), ('slip_id', '=', doc.id)],  limit=1).total or 0.0,
            }

            data.append(val)

        return{
            'docs': docs,
            'data': data,
        }
