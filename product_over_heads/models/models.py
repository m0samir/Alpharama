from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,UserError


class ProductOverHeads(models.Model):
    _name = 'product.overheads'
    _inherit = 'mail.thread'
    _rec_name = "from_date"
    
    from_date = fields.Date(string="From Date", required=True, track_visibility='onchange')  
    to_date = fields.Date(string="To Date", required=True, track_visibility='onchange')
    total_amount = fields.Float("Total Amount", readonly=True, track_visibility='onchange')
    total_per_sft = fields.Float("Total Per SFT Amount", readonly=True, track_visibility='onchange')
    total_sft = fields.Float("Total SFT", required=False, track_visibility='onchange')
    overhead_product = fields.Many2one("product.template", required=False, track_visibility='onchange')
    product_oh_line_ids = fields.One2many('product.overheads.line', "product_overheads_id", copy=True)
            
    def update_product_cost(self):
        if not self.overhead_product:
            raise ValidationError(_('Please select "Overhead Product"'))
        if not self.total_sft or self.total_sft == 0:
            raise ValidationError(_('Please enter "Total SFT" Value'))
        self.total_amount = 0
        self.total_per_sft = 0
        for record in self:
            for rec in record.product_oh_line_ids:
                rec.per_sft = rec.amount / record.total_sft
                record.total_amount += rec.amount
                record.total_per_sft += rec.per_sft
        self.overhead_product.standard_price = self.total_per_sft
        
            
class ProductOverHeadsLine(models.Model):
    _name = 'product.overheads.line'
    _description = "Overheads Details"

    product_overheads_id = fields.Many2one("product.overheads")
    overhead_id = fields.Many2one('overhead.overhead', string="Overhead", required=True)
    amount = fields.Float(string="Amount", required=True)
    per_sft = fields.Float(string="Per SFT Amount", readonly=True)
        
    
class OverHeads(models.Model):
    _name = 'overhead.overhead'
    _rec_name = "name"

    name = fields.Char("Name", required=True)
