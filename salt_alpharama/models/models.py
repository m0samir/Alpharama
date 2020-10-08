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

                    
                    
class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    price_percentage = fields.Float(string='Price Percentage')
    
    @api.onchange('price_percentage')
    def update_price(self):
        for rec in self:
            rec.price = rec.product_tmpl_id.standard_price * (rec.price_percentage / 100)
            
            
class StockLocation(models.Model):
    _inherit = "stock.location"

    valuation_in_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Incoming)',
        help="Used for real-time inventory valuation. When set on a virtual location (non internal type), "
             "this account will be used to hold the value of products being moved from an internal location "
             "into this location, instead of the generic Stock Output Account set on the product. "
             "This has no effect for internal locations.")
