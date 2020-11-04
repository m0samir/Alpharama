from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from odoo import api, fields, models, _


class ProductOverHeads(models.Model):
    _name = 'product.overheads'
    _inherit = 'mail.thread'
    _rec_name = "from_date"
    
    from_date = fields.Date(string="From Date", required=True, track_visibility='onchange')  
    to_date = fields.Date(string="To Date", required=True, track_visibility='onchange')
    total_amount = fields.Float("Total Amount", compute="_onchange_product_oh_line_ids", readonly=True, track_visibility='onchange')
    total_per_sft = fields.Float("Total Per SFT Amount", compute="_onchange_product_oh_line_ids", readonly=True, track_visibility='onchange')
    product_oh_line_ids = fields.One2many('product.overheads.line', "product_overheads_id", copy=True)

    def _onchange_product_oh_line_ids(self):
        if self.product_oh_line_ids:
            self.total_amount = 0
            self.total_per_sft = 0
            for record in self:
                for rec in record.product_oh_line_ids:
                    record.total_amount += rec.amount
                    record.total_per_sft += rec.per_sft
            
            
class ProductOverHeadsLine(models.Model):
    _name = 'product.overheads.line'
    _description = "Overheads Details"

    product_overheads_id = fields.Many2one("product.overheads")
    overhead_id = fields.Many2one('overhead.overhead', string="Overhead", required=True)
    amount = fields.Float(string="Amount", required=True)
    per_sft = fields.Float(string="Per SFT Amount", required=True)
        
    
class OverHeads(models.Model):
    _name = 'overhead.overhead'
    _rec_name = "name"

    name = fields.Char("Name", required=True)
