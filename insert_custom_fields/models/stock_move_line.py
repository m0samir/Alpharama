from collections import Counter

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round, float_compare, float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"
    
    no_of_pieces = fields.Float(string="Pieces", store=True)
    mno_of_pieces = fields.Float(string="Pieces", store=True)

    @api.onchange('lot_id')
    def _pieces_auto_populate(self):
        for rec in self:
            if rec.lot_id:
                rec.mno_of_pieces = rec.lot_id.no_of_pieces
   

class StockPickingValidation(models.Model):
    _inherit = "stock.picking"
    
    # def button_validate(self):
        # for rec in self.move_line_ids_without_package:
# #             if rec.lot_id and rec.mno_of_pieces > rec.lot_id.no_of_pieces and rec.product_id:
# #                 rec.mno_of_pieces = rec.lot_id.no_of_pieces
# #                 raise ValidationError("Available Pieces are %s" % rec.lot_id.no_of_pieces)
            
            # if rec.lot_id and rec.mno_of_pieces <= rec.lot_id.no_of_pieces and rec.product_id:
                # rec.lot_id.no_of_pieces = rec.lot_id.no_of_pieces - rec.mno_of_pieces
                
        # self.ensure_one()
        # if not self.move_lines and not self.move_line_ids:
            # raise UserError(_('Please add some items to move.'))

        # # Clean-up the context key at validation to avoid forcing the creation of immediate
        # # transfers.
        # ctx = dict(self.env.context)
        # ctx.pop('default_immediate_transfer', None)
        # self = self.with_context(ctx)

        # # add user as a follower
        # self.message_subscribe([self.env.user.partner_id.id])

        # # If no lots when needed, raise error
        # picking_type = self.picking_type_id
        # precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        # no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        # no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.move_line_ids)
        # if no_reserved_quantities and no_quantities_done:
            # raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        # if picking_type.use_create_lots or picking_type.use_existing_lots:
            # lines_to_check = self.move_line_ids
            # if not no_quantities_done:
                # lines_to_check = lines_to_check.filtered(
                    # lambda line: float_compare(line.qty_done, 0,
                                               # precision_rounding=line.product_uom_id.rounding)
                # )

            # for line in lines_to_check:
                # product = line.product_id
                # if product and product.tracking != 'none':
                    # if not line.lot_name and not line.lot_id:
                        # raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        # # Propose to use the sms mechanism the first time a delivery
        # # picking is validated. Whatever the user's decision (use it or not),
        # # the method button_validate is called again (except if it's cancel),
        # # so the checks are made twice in that case, but the flow is not broken
        # sms_confirmation = self._check_sms_confirmation_popup()
        # if sms_confirmation:
            # return sms_confirmation

        # if no_quantities_done:
            # view = self.env.ref('stock.view_immediate_transfer')
            # wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            # return {
                # 'name': _('Immediate Transfer?'),
                # 'type': 'ir.actions.act_window',
                # 'view_mode': 'form',
                # 'res_model': 'stock.immediate.transfer',
                # 'views': [(view.id, 'form')],
                # 'view_id': view.id,
                # 'target': 'new',
                # 'res_id': wiz.id,
                # 'context': self.env.context,
            # }

        # if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            # view = self.env.ref('stock.view_overprocessed_transfer')
            # wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            # return {
                # 'type': 'ir.actions.act_window',
                # 'view_mode': 'form',
                # 'res_model': 'stock.overprocessed.transfer',
                # 'views': [(view.id, 'form')],
                # 'view_id': view.id,
                # 'target': 'new',
                # 'res_id': wiz.id,
                # 'context': self.env.context,
            # }

        # # Check backorder should check for other barcodes
        # if self._check_backorder():
            # return self.action_generate_backorder_wizard()
        # self.action_done()
        # return
