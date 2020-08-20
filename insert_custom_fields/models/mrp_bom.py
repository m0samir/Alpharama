# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    work_order_operation = fields.Text(string='Operation', store=True)
    work_order_time = fields.Text(string='Time', store=True)
    work_order_comments = fields.Text(string='Comments', store=True)
    
