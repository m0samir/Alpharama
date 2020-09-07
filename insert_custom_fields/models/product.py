# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    pt_no_of_pieces = fields.Float(string='Total Pieces', store=True)
   
    
