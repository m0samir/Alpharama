# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    pt_no_of_pieces = fields.Float(related = 'product_variant_id.stock_move_ids.mno_of_pieces', string='Total Pieces', store=True)
   
    
