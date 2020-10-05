# Copyright 2020 omolonlsn@gmail.com
# License

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError


class LandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_bill = fields.Many2many('account.invoice', domain="[('number', 'like', 'BILL')]",
                                   string='Vendor Bills', states={'done': [('readonly', True)]})

    @api.multi
    def button_validate(self):
        self.compute_landed_cost()
        if any(cost.state != 'draft' for cost in self):
            raise UserError(_('Only draft landed costs can be validated'))
        if any(not cost.valuation_adjustment_lines for cost in self):
            raise UserError(_('No valuation adjustments lines. You should maybe recompute the landed costs.'))
        if not self._check_sum():
            raise UserError(_('Cost and adjustments lines do not match. You should maybe recompute the landed costs.'))

        for cost in self:
            move = self.env['account.move']
            move_vals = {
                'journal_id': cost.account_journal_id.id,
                'date': cost.date,
                'ref': cost.name,
                'line_ids': [],
            }
            for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                # Prorate the value at what's still in stock
                cost_to_add = (line.move_id.remaining_qty / line.move_id.product_qty) * line.additional_landed_cost

                new_landed_cost_value = line.move_id.landed_cost_value + line.additional_landed_cost
                line.move_id.write({
                    'landed_cost_value': new_landed_cost_value,
                    'value': line.move_id.value + line.additional_landed_cost,
                    'remaining_value': line.move_id.remaining_value + cost_to_add,
                    'price_unit': (line.move_id.value + line.additional_landed_cost) / line.move_id.product_qty,
                })
                # `remaining_qty` is negative if the move is out and delivered proudcts that were not
                # in stock.
                qty_out = 0
                if line.move_id._is_in():
                    qty_out = line.move_id.product_qty - line.move_id.remaining_qty
                elif line.move_id._is_out():
                    qty_out = line.move_id.product_qty
                move_vals['line_ids'] += line._create_accounting_entries(move, qty_out)

            move = move.create(move_vals)
            cost.write({'state': 'done', 'account_move_id': move.id})
            move.post()
        return True

    def get_valuation_lines(self):
        lines = []

        for move in self.mapped('picking_ids').mapped('move_lines'):
            # it doesn't make sense to make a landed cost for a product that isn't set as being valuated in real time at real cost
            if move.product_id.valuation != 'real_time' or move.product_id.cost_method != 'fifo':
                continue
            # product_total_cost=move.value+
            vals = {
                'product_id': move.product_id.id,
                'move_id': move.id,
                'quantity': move.product_qty,
                'former_cost': move.value,
                'weight': move.product_id.weight * move.product_qty,
                'volume': move.product_id.volume * move.product_qty,

            }
            lines.append(vals)

        if not lines and self.mapped('picking_ids'):
            raise UserError(_(
                "You cannot apply landed costs on the chosen transfer(s). Landed costs can only be applied for products with automated inventory valuation and FIFO costing method."))
        return lines

    @api.multi
    def compute_landed_cost(self):
        for rec in self:
            rec.cost_lines.unlink()
            for bill in rec.vendor_bill.ids:
                bill_record = rec.env['account.invoice'].search([('id', '=', bill)], limit=1)
                if bill_record:
                    for line in bill_record.invoice_line_ids:
                        if line.product_id.landed_cost_ok:
                            rec.env['stock.landed.cost.lines'].create({
                                'product_id': line.product_id.id,
                                'name': line.product_id.name or '',
                                'split_method': line.product_id.split_method or 'equal',
                                'price_unit': line.product_id.standard_price or 0.0,
                                'account_id': line.product_id.property_account_expense_id.id or line.product_id.categ_id.property_account_expense_categ_id.id,
                                'cost_id': rec.id
                            })

        AdjustementLines = self.env['stock.valuation.adjustment.lines']
        AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()

        digits = dp.get_precision('Product Price')(self._cr)
        towrite_dict = {}
        for cost in self.filtered(lambda cost: cost.picking_ids):
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            for val_line_values in all_val_line_values:
                for cost_line in cost.cost_lines:
                    val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                    self.env['stock.valuation.adjustment.lines'].create(val_line_values)
                total_qty += val_line_values.get('quantity', 0.0)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += tools.float_round(former_cost, precision_digits=digits[1]) if digits else former_cost

                total_line += 1

            for line in cost.cost_lines:
                value_split = 0.0
                for valuation in cost.valuation_adjustment_lines:
                    value = 0.0
                    if valuation.cost_line_id and valuation.cost_line_id.id == line.id:
                        if line.split_method == 'by_quantity' and total_qty:
                            per_unit = (line.price_unit / total_qty)
                            value = valuation.quantity * per_unit
                        elif line.split_method == 'by_weight' and total_weight:
                            per_unit = (line.price_unit / total_weight)
                            value = valuation.weight * per_unit
                        elif line.split_method == 'by_volume' and total_volume:
                            per_unit = (line.price_unit / total_volume)
                            value = valuation.volume * per_unit
                        elif line.split_method == 'equal':
                            value = (line.price_unit / total_line)
                        elif line.split_method == 'by_current_cost_price' and total_cost:
                            per_unit = (line.price_unit / total_cost)
                            value = valuation.former_cost * per_unit
                        else:
                            value = (line.price_unit / total_line)

                        if digits:
                            value = tools.float_round(value, precision_digits=digits[1], rounding_method='UP')
                            fnc = min if line.price_unit > 0 else max
                            value = fnc(value, line.price_unit - value_split)
                            value_split += value

                        if valuation.id not in towrite_dict:
                            towrite_dict[valuation.id] = value
                        else:
                            towrite_dict[valuation.id] += value

        product_list = []
        for key, value in towrite_dict.items():
            product_id = AdjustementLines.browse(key).product_id.id
            if product_id in product_list:
                # search_domain=[('cost_id','=', AdjustementLines.browse(key).cost_id.id),('product_id','=',product_id),]
                # id_list=self.env['stock.valuation.adjustment.lines'].search(search_domain).ids
                # last_id = id_list[0]
                AdjustementLines.browse(key).write({'additional_landed_cost': value,
                                                    'product_total_cost': AdjustementLines.browse(
                                                        key - 1).product_total_cost + value})
            else:
                product_list.append(AdjustementLines.browse(key).product_id.id)
                AdjustementLines.browse(key).write({'additional_landed_cost': value,
                                                    'product_total_cost': value + AdjustementLines.browse(
                                                        key).former_cost})

        count = 0
        for rec in self.valuation_adjustment_lines:
            count += 1
            if count == len(self.cost_lines) and rec.quantity != 0:
                rec.landed_unit_rate = rec.product_total_cost / rec.quantity
                count = 0

        return True


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    product_total_cost = fields.Float(
        string='Total Cost',
        store=True,
    )

    landed_unit_rate = fields.Float(
        string='Unit Rate',
    )
