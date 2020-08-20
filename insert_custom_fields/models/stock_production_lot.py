from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    pno_of_pieces = fields.Float(string='Total Pieces')
    no_of_pieces = fields.Float(string='Available Pieces', store=True)
    valid_boolean = fields.Boolean("Component", default=False)
    
     #def _product_pieces(self):
        # for lot in self:
            # if lot.no_of_pieces == 0 and not lot.valid_boolean:
                # record = self.env['stock.move'].search([('lot_id.name', '=', lot.name), ('move_id.product_id', '=', lot.product_id.id)], limit=1)
                # lot.pno_of_pieces = lot.no_of_pieces = record.mno_of_pieces
                # lot.valid_boolean = True
                
            # else:
                # record = self.env['stock.move'].search([('lot_id.name', '=', lot.name), ('move_id.product_id', '=', lot.product_id.id)], limit=1)
                # lot.pno_of_pieces = record.mno_of_pieces
