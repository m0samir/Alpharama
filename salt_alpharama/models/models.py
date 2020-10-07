# Copyright 2020 omolonlsn@gmail.com
# License

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError


class LandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    internal_transfer = fields.Many2one('stock.picking', domain="[('name', 'like', '/INT/')]",
                                   string='Internal Transfer', states={'done': [('readonly', True)]})
    
    def compute_internal_transfer(self):
        for rec in self:
            if rec.internal_transfer:
                rec.cost_lines.unlink()
                for record in rec.internal_transfer.move_line_ids_without_package:
                    self.env['stock.landed.cost.lines'].create({
                    'product_id': record.product_id.id,
                    'name': record.product_id.name or '',
                    'split_method': 'equal',
                    'price_unit': record.product_id.standard_price * record.qty_done or 0.0,
                    'account_id': record.product_id.property_account_expense_id.id or       record.product_id.categ_id.property_account_expense_categ_id.id,
                    'cost_id': rec.id,
                    })  
