# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _, SUPERUSER_ID




class StockMove(models.Model):
    _inherit = 'stock.move'

    pwork_order_operation= fields.Text(related = 'bom_line_id.work_order_operation', string='Operations')
    pwork_order_time = fields.Text(related = 'bom_line_id.work_order_time', string='Time')
    pwork_order_comments = fields.Text(related = 'bom_line_id.work_order_comments', string='Comments')
    pwork_order_qconsumed = fields.Text(string='Actual Quantity Consumed')
    work_order_pieces = fields.Float(related = 'bom_line_id.no_of_pieces', string='Pieces')
    work_order_dozens = fields.Float(string='Dozens')
    work_order_sqft = fields.Float(string='Square Feets')
