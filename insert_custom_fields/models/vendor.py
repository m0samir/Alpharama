from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    vendor_type = fields.Selection([('Local', 'Local'), ('Import', 'Import'), ('Branch', 'Branch')], string='Vendor Type', required=True)
