# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from markupsafe import Markup


class SaleCopyWizard(models.TransientModel):
    _name = 'sale.copy.wizard'
    _description = 'Copy sale order to another company'

    sale_order_ids = fields.Many2many(
        'sale.order',
        string='Source Orders',
        required=True,
        readonly=True,
    )
    target_company_id = fields.Many2one(
        'res.company',
        string='Target Company',
        required=True,
        domain="[('id', '!=', current_company_id)]",
    )
    current_company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
    )
    copy_notes = fields.Boolean(
        string='Copy Notes',
        default=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids') or (
            [self.env.context['active_id']] if self.env.context.get('active_id') else []
        )
        if active_ids:
            res['sale_order_ids'] = [(6, 0, active_ids)]
        return res

    def action_copy_to_company(self):
        self.ensure_one()
        target_company = self.target_company_id

        if target_company not in self.env.user.company_ids:
            raise UserError(_(
                "You don't have access to company %s. "
                "Please contact your administrator."
            ) % target_company.name)

        copied_orders = []

        # Détecter les noms de champs selon la version Odoo
        # v19+ utilise product_uom_id et tax_ids
        # v16/17/18 utilise product_uom et tax_id
        SaleOrderLine = self.env['sale.order.line']
        uom_field_name = 'product_uom_id' if 'product_uom_id' in SaleOrderLine._fields else 'product_uom'
        tax_field_name = 'tax_ids' if 'tax_ids' in SaleOrderLine._fields else 'tax_id'

        for source in self.sale_order_ids:
            partner = source.partner_id

            new_order_vals = {
                'company_id': target_company.id,
                'partner_id': partner.id,
                'partner_invoice_id': source.partner_invoice_id.id,
                'partner_shipping_id': source.partner_shipping_id.id,
                'validity_date': source.validity_date,
                'payment_term_id': source.payment_term_id.id if source.payment_term_id else False,
                'note': source.note if self.copy_notes else False,
                'intercompany_origin_id': source.id,
                'origin': source.name,
                'team_id': False,
                'user_id': False,
            }

            new_order = self.env['sale.order'].sudo().with_company(target_company).create(new_order_vals)

            for line in source.order_line:
                # Sections et notes
                if line.display_type:
                    self.env['sale.order.line'].sudo().with_company(target_company).create({
                        'order_id': new_order.id,
                        'name': line.name,
                        'display_type': line.display_type,
                        'sequence': line.sequence,
                    })
                    continue

                if line.product_id:
                    product = line.product_id.sudo()
                    if not product.active:
                        product.sudo().write({'active': True})

                    existing = self.env['product.product'].sudo().with_company(
                        target_company
                    ).search([('id', '=', line.product_id.id)], limit=1)

                    if not existing:
                        product_vals = {
                            'name': line.product_id.name,
                            'type': line.product_id.type,
                            'uom_id': line.product_id.uom_id.id,
                            'uom_po_id': line.product_id.uom_po_id.id,
                            'list_price': line.price_unit,
                            'company_id': False,
                        }
                        self.env['product.product'].sudo().create(product_vals)

                line_vals = {
                    'order_id': new_order.id,
                    'product_id': line.product_id.id if line.product_id else False,
                    'name': line.name,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'discount': line.discount,
                    'sequence': line.sequence,
                }

                # purchase_price est un champ de sale_margin — optionnel
                if hasattr(line, 'purchase_price'):
                    line_vals['purchase_price'] = line.purchase_price

                # Compatibilité v16/17/18 (product_uom) et v19+ (product_uom_id)
                uom = getattr(line, uom_field_name, None)
                if uom:
                    line_vals[uom_field_name] = uom.id

                new_line = self.env['sale.order.line'].sudo().with_company(target_company).create(line_vals)

                if line.product_id:
                    product_target = line.product_id.with_company(target_company)
                    # Compatibilité v16/17/18 (taxes_id) et v19+ (tax_ids sur product)
                    product_taxes = getattr(product_target, 'taxes_id', None) or getattr(product_target, 'tax_ids', None)
                    if product_taxes:
                        taxes = product_taxes.filtered(
                            lambda t: t.company_id == target_company
                        )
                        new_line.sudo().write({tax_field_name: [(6, 0, taxes.ids)]})

            # Recalcul des marges si le module sale_margin est installé
            for line in new_order.order_line:
                if hasattr(line, '_compute_margin'):
                    line.sudo()._compute_margin()

            # Message dans le chatter du devis source
            source.sudo().message_post(
                body=Markup(
                    'Order copied to <b>%s</b> on %s by <b>%s</b>.<br/>'
                    'Reference of copied order: <a href="/web#id=%s&model=sale.order&view_type=form">%s</a>'
                ) % (
                    target_company.name,
                    fields.Datetime.now().strftime('%d/%m/%Y %H:%M'),
                    self.env.user.name,
                    new_order.id,
                    new_order.name,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

            copied_orders.append(new_order.name)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Copy successful'),
                'message': _('%s order(s) copied to %s: %s') % (
                    len(copied_orders),
                    target_company.name,
                    ', '.join(copied_orders),
                ),
                'type': 'success',
                'sticky': True,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    @api.model
    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Copy to Another Company'),
            'res_model': 'sale.copy.wizard',
            'view_mode': 'form',
            'target': 'new',
        }