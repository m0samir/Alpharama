from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    expected_arrival = fields.Datetime(string='Expected Arrival')
    

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    expected_arrival = fields.Datetime(string='Expected Arrival', compute='get_expected_arrival')
    
    def get_expected_arrival(self):
        po_number = self.env['purchase.order'].search([('name', '=', self.origin)])
        self.expected_arrival = po_number.expected_arrival