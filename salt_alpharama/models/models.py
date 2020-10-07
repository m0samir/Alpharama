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
