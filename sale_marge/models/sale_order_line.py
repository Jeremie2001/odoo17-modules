from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MargeOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_produit = fields.Float("  ", compute='_compute_margin', digits='Product Price', store=True,
                                  groups="base.group_user")
    margin_produit_copy = fields.Float("Marge", digits='Product Price', store=True, groups="base.group_user")

    margin_pourcent = fields.Float(
        "  ", compute='_compute_margin', store=True, groups="base.group_user", precompute=True)

    marge_percent_copy = fields.Float("Marge.%", store=True, groups="base.group_user")

    purchase_price = fields.Float(
        string="Coût", compute="_compute_purchase_price",
        digits='Product Price', store=True, readonly=False, copy=False, precompute=True,
        groups="base.group_user")

    qty_delivered_percent = fields.Float(
        string="Délivré.%",
        default=0.0,
        store=True, readonly=True, copy=False)

    is_marge_global = fields.Boolean(related='order_id.is_marge_global', store=True, readonly=True)

    marge_reduit = fields.Float("Marge R", compute='_compute_marge_reduite', store=True, readonly=True)
    marge_reduit_percent = fields.Float("Marge R.%", store=True, readonly=True)

    @api.depends('price_unit', 'discount', 'purchase_price')
    def _compute_marge_reduite(self):
        for line in self:
            if line.discount:
                line.marge_reduit = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
                line.marge_reduit_percent = line.marge_reduit/line.price_subtotal if line.price_subtotal != 0 else 0
            else:
                line.marge_reduit = line.margin_produit_copy
                line.marge_reduit_percent = line.marge_percent_copy

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_purchase_price(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)

            # Convert the cost to the line UoM
            product_cost = line.product_id.uom_id._compute_price(
                line.product_id.standard_price,
                line.product_uom,
            )

            line.purchase_price = line._convert_to_sol_currency(
                product_cost,
                line.product_id.cost_currency_id)

    # 2
    @api.depends('price_unit', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:

            line.margin_produit = line.purchase_price and (line.price_unit * line.product_uom_qty) - (line.purchase_price * line.product_uom_qty)
            line.margin_produit_copy = line.purchase_price and (line.price_unit * line.product_uom_qty) - (line.purchase_price * line.product_uom_qty)

            line.margin_pourcent = line.price_unit and line.margin_produit / (line.price_unit * line.product_uom_qty)
            line.marge_percent_copy = line.price_unit and line.margin_produit / (line.price_unit * line.product_uom_qty)

    # 3
    @api.onchange('margin_produit_copy')
    def _onchange_marge_product(self):
        for line in self:
            if line.purchase_price <= 0 and line.product_id:
                line.margin_produit_copy = 0.0
                return {
                    'warning': {
                        'title': "Erreur de validation",
                        'message': "Le coût du produit doit être supérieur à 0.",
                    }
                }

            if line.product_uom_qty:
                line.price_unit = line.purchase_price + (line.margin_produit_copy / line.product_uom_qty)

            else:
                line.product_uom_qty = line.margin_produit_copy / (line.price_unit - line.purchase_price) if line.purchase_price else 0

    # 1
    @api.onchange('marge_percent_copy')
    def onchange_margin_percent(self):
        for line in self:
            if line.purchase_price <= 0 and line.product_id:
                line.marge_percent_copy = 0.0
                line.margin_pourcent = 0.0
                return {
                    'warning': {
                        'title': "Erreur de validation",
                        'message': "Le coût du produit doit être supérieur à 0.",
                    }
                }

            if line.marge_percent_copy:  # and line.purchase_price > 0
                line.price_unit = line.purchase_price / (1 - line.marge_percent_copy)

            else:
                line.margin_produit_copy = 0
                line.price_unit = line.purchase_price



    @api.onchange('product_id')
    def onchange_product_set_default_marge_percent(self):
        for line in self:
            if line.product_id and line.name and "Remise" not in line.name:
                # Définir directement le prix unitaire basé sur le coût + 35%
                if line.purchase_price > 0:
                    line.price_unit = line.purchase_price / (1 - 0.35)
                # Forcer la marge à 35%
                line.marge_percent_copy = 0.35
                line.margin_pourcent = 0.35

    # Cette fonction permet de garder la valeur du prix unitaire quand la qty change. Elle empêche la reprise du prix(au niveau du prod)
    @api.onchange('product_uom_qty')
    def onchange_qty(self):
        for line in self:
            line.price_unit = line.purchase_price / (1 - line.marge_percent_copy)
