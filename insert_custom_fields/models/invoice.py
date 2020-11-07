from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'account.move'
    
    payment_tags = fields.Many2many('payment.tags', string='Payment Tags')
    
class PaymentTags(models.Model):
    _name = 'payment.tags'
    
    name = fields.Char(string='Tag Name')
