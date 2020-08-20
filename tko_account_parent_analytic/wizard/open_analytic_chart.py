# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from odoo import models, fields, api,_


class OpenAnalyticAccount(models.TransientModel):
    """
    For Chart of Accounts
    """
    _name = "open.analytic.account"
    _description = "Open Analytic Accounts"

    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    
    def _build_contexts(self, data):
        result = {}
        if data['target_move'] == 'posted':
            result['move_state'] = data['target_move']
        result['date_from'] = data['date_from'] or False
        result['date_to'] = data['date_to'] or False
        result['show_parent_account'] = True
        result['company_id'] = self.env.user.sudo().company_id.id
        return result

    @api.multi
    def account_chart_open_window(self):
        """
        Opens chart of Accounts
        @return: dictionary of Open account chart window on given date(s) and all Entries or posted entries
        """
        self.ensure_one()
        data = self.read([])[0]
        used_context = self._build_contexts(data)
        self  = self.with_context(used_context)
        if self.env['account.analytic.account'].search([('parent_id','!=',False)],limit=1):
            result = self.env.ref('tko_account_parent_analytic.open_view_analytic_account_tree').read([])[0]
        else:
            result = self.env.ref('tko_account_parent_analytic.open_view_analytic_account_noparent_tree').read([])[0]
        result_context = eval(result.get('context','{}')) or {}
        used_context.update(result_context)
        result['context'] = str(used_context)
        return result


# class WizardMultiChartsAccounts(models.TransientModel):
#     _inherit = 'wizard.multi.charts.accounts'
#
#     @api.multi
#     def execute(self):
#         res = super(WizardMultiChartsAccounts, self).execute()
#         self.chart_template_id.update_generated_account({},self.code_digits,self.company_id)
#         return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
