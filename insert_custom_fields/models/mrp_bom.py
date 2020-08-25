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
    no_of_pieces = fields.Float(String = 'Number of Pieces', store=True )
    
    
class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    tot_pieces = fields.Float(string='Total Pieces Manufactured', compute='_total_pieces_all')
    
    @api.depends('bom_line_ids.no_of_pieces')
    def _total_pieces_all(self):
        """
        Compute the total Pieces of the SO.
        """
        mrp_bom_obj=self.env['mrp.bom'].search([('product_tmpl_id.name','=','Raw Hides Selection')])
        for piece in self:
            total_pieces = total_pieces2= 0.0
            for line in piece.bom_line_ids:
                if line.product_tmpl_id.name=='Pre-Tanning Manufacture':
                    if mrp_bom_obj:
                        total_pieces+=mrp_bom_obj[0].tot_pieces
                        total_pieces2=total_pieces/2
                else:
                    
                #amount_untaxed += line.price_subtotal
                    total_pieces += line.no_of_pieces
            piece.update({
                'tot_pieces': total_pieces2 or total_pieces,
                
            })
    
