from odoo import models, fields, api

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def get_product_ids_from_quotation(self, order_id: int):
        order = self.env['sale.order'].browse(order_id)
        return order.order_line.mapped('product_id.product_tmpl_id').ids

    @api.onchange('body')
    def _onchange_body(self):
        if self._context.get('default_model') == 'sale.order':
            additional_attachments = []

            
            order_id = self._context.get('default_res_id') or self._context.get('active_id')
            if order_id:
                order = self.env['sale.order'].browse(order_id)
                if order.exists():
                    product_ids = self.get_product_ids_from_quotation(order.id)
                    additional_attachments = self.env['ir.attachment'].search([
                        ('res_model', '=', 'product.template'),
                        ('res_id', 'in', product_ids)
                    ])

            if additional_attachments:
                self.attachment_ids |= additional_attachments

