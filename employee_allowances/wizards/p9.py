from odoo import models, api, fields
from datetime import datetime, timedelta, date


def get_years():
    year_list = []
    current_year = datetime.now().year
    for i in range(current_year-10, int(current_year)+1):
        year_list.append((str(i), str(i)))
    return year_list


class HrP9Form(models.TransientModel):
    _name = 'hr.p9.form'
    _description = 'Employee P9 Form'

    year = fields.Selection(get_years(), string='Year',
                            required=True, default=str(datetime.now().year-1))
    employee_ids = fields.Many2many('hr.employee', string='Employees')

    def generate_p9_forms(self):
        start_date = date(int(self.year), 1, 1)
        end_date = date(int(self.year), 12, 31)

        data = {'model': 'hr.payslip'}

        for rec in self.employee_ids:
            payslips = self.env['hr.payslip'].search(
                [('employee_id', '=', rec.id), ('state', 'in', ['draft']), ('date_from', '>=', start_date), ('date_from', '<=', end_date)]).mapped('line_ids')

        return self.env.ref('employee_allowances.action_employee_p9_report').report_action(self, data=data)


class SingleP9(models.TransientModel):
    _name = 'single.p9.form'
    _description = 'Single employee P9 Form'

    year = fields.Selection(get_years(), string='Year',
                            required=True, default=str(datetime.now().year-1))

    def generate_p9_forms(self):
        active_ids = self._context.get('active_ids')

        employee = self.env['hr.employee'].search_read(
            [('id', '=', active_ids[0])], fields={'name', 'company_id', 'tax_pin'})[0]
        company_vat = self.env['res.company'].search(
            [('id', '=', employee['company_id'][0])]).mapped('vat')[0]
        payslips = self.env['hr.payslip'].search_read([(
            'employee_id', '=', active_ids[0]), ('date_from', '>=', f'01-01-{self.year}'), ('date_from', '<=', f'31-12-{self.year}')], fields={'line_ids', 'date_from'})
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        ms = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
              '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

        letters = ['A', 'B', 'C', 'D', 'E1', 'E2',
                   'E3', 'F', 'G', 'H', 'J', 'K', 'L']
        data = {
            'employee': {
                'name': employee['name'],
                'vat': employee['tax_pin'],
            },
            'ms': ms,
            'employer': {'vat': company_vat if company_vat else None, 'name': employee['company_id'][1]},
            'body': {},
        }
        for m in ms:
            # data['body'][m] = [0 for i in range(14)]
            data['body'][m] = {}
            for l in letters:
                data['body'][m][l] = 0

        for slip in payslips:
            month = slip['date_from'].strftime('%m')
            if slip['line_ids']:
                payslip_line = self.env['hr.payslip.line']
                basic = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule10').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                gross = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule30').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                pension = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule66').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                nssf = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule55').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                gross_taxable = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule45').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                paye = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule105').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                relief = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule91').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                insurance_relief = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule96').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                net_pay = payslip_line.search_read(
                    [('slip_id', '=', slip['id']), ('salary_rule_id', '=', self.env.ref(
                        'hr_ke.ke_rule120').id)],
                    limit=1,
                    fields={'total'}
                ) or 0.0
                insurance_relief = insurance_relief[0]['total'] if type(
                    insurance_relief) == list else 0.0
                relief = relief[0]['total'] if type(relief) == list else 0.0
                data['body'][month]['A'] = basic[0]['total']
                data['body'][month]['D'] = gross[0]['total']
                data['body'][month]['E1'] = 0.3*gross[0]['total']
                data['body'][month]['E2'] = pension[0]['total'] if type(
                    pension) == list else 0.0
                data['body'][month]['E3'] = nssf[0]['total'] if type(
                    nssf) == list else 0.0
                data['body'][month]['G'] = nssf[0]['total'] if type(
                    nssf) == list else 0.0
                data['body'][month]['H'] = gross_taxable[0]['total'] if type(
                    gross_taxable) == list else 0.0
                data['body'][month]['J'] = paye[0]['total'] if type(
                    paye) == list else 0.0

                data['body'][month]['K'] = relief + insurance_relief
                data['body'][month]['L'] = net_pay[0]['total'] if type(
                    net_pay) == list else 0.0

        seen = {}
        # Calculate column totals
        for i in data['body']:
            for j in data['body'][i]:
                if j in seen:
                    seen[j] += data['body'][i][j]
                else:
                    seen[j] = data['body'][i][j]

        data['totals'] = [seen[i] for i in sorted(seen)]
        return self.env.ref('employee_allowances.action_employee_p9_report').report_action(self, data=data)
