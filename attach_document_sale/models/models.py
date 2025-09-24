from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def get_product_ids_from_quotation(self, order_id: int):
        """Récupère les IDs des modèles de produits d'une commande"""
        order = self.env['sale.order'].browse(order_id)
        if not order.exists():
            return []
        # Plus efficace avec ids directement
        return order.order_line.mapped('product_id.product_tmpl_id.id')

    @api.onchange('body')
    def _onchange_body(self):
        if self._context.get('default_model') != 'sale.order':
            return

        # Vérifications de sécurité
        if not self.attachment_ids:
            return

        try:
            # Extraction du nom de commande
            file_name = self.attachment_ids[0].name
            if '-' not in file_name or '.' not in file_name:
                _logger.warning(f"Format de fichier inattendu : {file_name}")
                return
                
            order_name = file_name.split('-')[1].split('.')[0].strip()
            
            # Recherche de la commande
            order = self.env['sale.order'].search([('name', '=', order_name)], limit=1)
            if not order:
                _logger.warning(f"Commande non trouvée : {order_name}")
                return

            # Récupération des pièces jointes des produits
            product_ids = self.get_product_ids_from_quotation(order.id)
            if product_ids:
                additional_attachments = self.env['ir.attachment'].search([
                    ('res_model', '=', 'product.template'),
                    ('res_id', 'in', product_ids)
                ])
                
                # Ajout des pièces jointes (évite les doublons)
                self.attachment_ids = (self.attachment_ids | additional_attachments)
                
        except (IndexError, AttributeError) as e:
            _logger.error(f"Erreur lors du traitement des pièces jointes : {e}")
