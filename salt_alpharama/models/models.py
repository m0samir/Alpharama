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
    
    def compute_internal_transfer(self):
        for rec in self:
            if rec.internal_transfer:
                rec.cost_lines.unlink()
                for record in rec.internal_transfer.move_line_ids_without_package:
                    vendor_price = self.env['product.supplierinfo'].search([('name', '=', rec.internal_transfer.partner_id.name), ('product_tmpl_id.name', '=', record.product_id.name)], limit=1)
                    self.env['stock.landed.cost.lines'].create({
                    'product_id': record.product_id.id,
                    'name': record.product_id.name or '',
                    'split_method': 'equal',
                    'price_unit': (record.product_id.standard_price - vendor_price.price) * record.qty_done or 0.0 if vendor_price else record.product_id.standard_price * record.qty_done or 0.0,
                    'account_id': record.product_id.property_account_expense_id.id or       record.product_id.categ_id.property_account_expense_categ_id.id,
                    'cost_id': rec.id,
                    })  

                    
                    
class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    price_percentage = fields.Float(string='Price Percentage')
    
    @api.onchange('price_percentage')
    def update_price(self):
        for rec in self:
            rec.price = rec.product_tmpl_id.standard_price * (rec.price_percentage / 100)
            
            
class StockLocation(models.Model):
    _inherit = "stock.location"

    valuation_in_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Incoming)',
        domain=[('deprecated', '=', False)],
        help="Used for real-time inventory valuation. When set on a virtual location (non internal type), "
             "this account will be used to hold the value of products being moved from an internal location "
             "into this location, instead of the generic Stock Output Account set on the product. "
             "This has no effect for internal locations.")

    
class StockMove(models.Model):
    _inherit = "stock.move"
    
    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries """
        self.ensure_one()
        if self.product_id.type != 'product':
            # no stock valuation for consumable products
            return False
        if self.restrict_partner_id:
            # if the move isn't owned by the company, we don't make any valuation
            return False

        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False

        # Create Journal Entry for products arriving in the company; in case of routes making the link between several
        # warehouse of the same company, the transit location belongs to this company, so we don't need to create accounting entries
        if self._is_in():
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_from and location_from.usage == 'customer':  # goods returned from customer
                self.with_context(force_company=company_to.id)._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)
            else:
                self.with_context(force_company=company_to.id)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)

        # Create Journal Entry for products leaving the company
        if self._is_out():
            
            vendor_price = self.env['product.supplierinfo'].search([('name', '=', self.picking_id.partner_id.name), ('product_tmpl_id.name', '=', self.product_id.name)], limit=1)
            
            if vendor_price and vendor_price != 0:
                cost = -1 * (( cost / self.product_id.standard_price ) * vendor_price.price)
            else:
                cost = -1 * cost      
            
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_to and location_to.usage == 'supplier':  # goods returned to supplier
                self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
            else:
                self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)

        if self.company_id.anglo_saxon_accounting:
            # Creates an account entry from stock_input to stock_output on a dropship move. https://github.com/odoo/odoo/issues/12687
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if self._is_dropshipped():
                if cost > 0:
                    self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)
                else:
                    cost = -1 * cost
                    self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)
            elif self._is_dropshipped_returned():
                if cost > 0:
                    self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_valuation, acc_src, journal_id, qty, description, svl_id, cost)
                else:
                    cost = -1 * cost
                    self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_dest, acc_valuation, journal_id, qty, description, svl_id, cost)

        if self.company_id.anglo_saxon_accounting:
            #eventually reconcile together the invoice and valuation accounting entries on the stock interim accounts
            self._get_related_invoices()._stock_account_anglo_saxon_reconcile_valuation(product=self.product_id)
            
            
class SkinSaltMaster(models.Model):
    _name = 'skin.salt.master'
    _rec_name = 'skin_type'
    _inherit = 'mail.thread'
    
    skin_type = fields.Many2one('product.product', string='Skin Type', track_visibility='onchange')
    salt_qty = fields.Float('Salt Quantity', track_visibility='onchange')
    
    
class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    purchase_order = fields.Many2one('stock.picking', 'Purchase Order')
    

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
                    
    @api.onchange('product_id', 'product_uom_id')
    def onchange_product_id(self):
        if self.picking_id.purchase_order and self.product_id:
            for rec in self.picking_id.purchase_order.move_ids_without_package:
                skin_salt_qty = self.env['skin.salt.master'].search([('skin_type', '=', rec.product_id.id)], limit=1)
                if skin_salt_qty:
                    self.qty_done = skin_salt_qty.salt_qty * rec.quantity_done
                else:
                    self.qty_done = 0
        if self.product_id:
            if not self.id and self.user_has_groups('stock.group_stock_multi_locations'):
                self.location_dest_id = self.location_dest_id._get_putaway_strategy(self.product_id) or self.location_dest_id
            if self.picking_id:
                product = self.product_id.with_context(lang=self.picking_id.partner_id.lang or self.env.user.lang)
                self.description_picking = product._get_description(self.picking_id.picking_type_id)
            self.lots_visible = self.product_id.tracking != 'none'
            if not self.product_uom_id or self.product_uom_id.category_id != self.product_id.uom_id.category_id:
                if self.move_id.product_uom:
                    self.product_uom_id = self.move_id.product_uom.id
                else:
                    self.product_uom_id = self.product_id.uom_id.id
            res = {'domain': {'product_uom_id': [('category_id', '=', self.product_uom_id.category_id.id)]}}
        else:
            res = {'domain': {'product_uom_id': []}}
        return res
    

class ProductTemplate(models.Model):
    _inherit="product.template"
    
    def set_access_for_product(self):
        self.able_to_see_product_cost = self.env['res.users'].has_group('salt_alpharama.group_cost_access')

    able_to_see_product_cost = fields.Boolean(default=False, compute='set_access_for_product', string='Is user able to modify product?')
