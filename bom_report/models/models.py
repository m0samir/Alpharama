# -*- coding: utf-8 -*-

from odoo import models, fields


# class bom_report(models.Model):
#     _inherit = 'mrp.production'
#     _description = 'Print Bom Lot Reports '


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Extend Products Model'

    isa_hide = fields.Boolean(string='Is a Hide')
