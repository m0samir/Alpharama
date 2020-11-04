from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from odoo import api, fields, models, _


class ProductOverHeads(models.Model):
    _name = 'product.overheads'
    _inherit = 'mail.thread'
    _rec_name = "from_date"
    
    from_date = fields.Date(string="From Date")  
    to_date = fields.Date(string="To Date")
    total_amount = fields.Float("Total Amount")
    total_per_sft = fields.Float("Total Per SFT Amount")
    product_oh_line_ids = fields.One2many('product.overheads.line', "product_overheads_id", copy=True)

    
class ProductOverHeadsLine(models.Model):
    _name = 'product.overheads.line'
    _description = "Overheads Details"

    product_overheads_id = fields.Many2one("product.overheads")
    overhead_id = fields.Many2one('overhead.overhead', string="Overhead")
    amount = fields.Float(string="Amount")
    per_sft = fields.Float(string="Per SFT Amount")
    
class OverHeads(models.Model):
    _name = 'overhead.overhead'
    _rec_name = "name"

    name = fields.Char("Name")