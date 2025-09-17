from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def _copy_attachments_to_product_template(self):
        """Copie tous les documents des composants vers le produit final"""
        Attachment = self.env['ir.attachment']
        ProductDocument = self.env['product.document']
        
        for bom in self:
            if not bom.product_tmpl_id:
                continue
                
            # Produit final (le conteneur)
            product_template = bom.product_tmpl_id
            _logger.info(f"Synchronisation BoM {bom.id} vers produit {product_template.name}")

            for line in bom.bom_line_ids:
                product = line.product_id
                template = product.product_tmpl_id

                # Fichiers attachés au niveau variant
                product_attachments = Attachment.search([
                    ('res_model', '=', 'product.product'),
                    ('res_id', '=', product.id),
                ])

                # Fichiers attachés au niveau template
                template_attachments = Attachment.search([
                    ('res_model', '=', 'product.template'),
                    ('res_id', '=', template.id),
                ])

                all_attachments = product_attachments | template_attachments

                for att in all_attachments:
                    # Vérifier si le document existe déjà (par name ET checksum pour éviter les doublons)
                    existing_attachment = Attachment.search([
                        ('res_model', '=', 'product.template'),
                        ('res_id', '=', product_template.id),
                        ('name', '=', att.name),
                        ('checksum', '=', att.checksum),
                    ], limit=1)
                    
                    if not existing_attachment:
                        try:
                            # Copier l'attachement
                            new_attachment = att.copy({
                                'res_model': 'product.template',
                                'res_id': product_template.id,
                            })

                            # Créer ou mettre à jour le document produit associé
                            product_doc = ProductDocument.search([
                                ('ir_attachment_id', '=', new_attachment.id),
                            ], limit=1)
                            
                            if product_doc:
                                product_doc.write({'attached_on': 'inside'})
                            else:
                                # Si pas de product.document, en créer un
                                ProductDocument.create({
                                    'ir_attachment_id': new_attachment.id,
                                    'attached_on': 'inside',
                                })
                                
                            _logger.info(f"Document copié: {att.name} vers {product_template.name}")
                            
                        except Exception as e:
                            _logger.error(f"Erreur lors de la copie du document {att.name}: {e}")

    @api.model_create_multi
    def create(self, vals_list):
        boms = super().create(vals_list)
        # Différer la synchronisation pour éviter les problèmes de commit
        boms.with_delay()._copy_attachments_to_product_template() if hasattr(boms, 'with_delay') else boms._copy_attachments_to_product_template()
        return boms

    def write(self, vals):
        res = super().write(vals)
        # Seulement si les lignes de BoM ont changé
        if 'bom_line_ids' in vals:
            self.with_delay()._copy_attachments_to_product_template() if hasattr(self, 'with_delay') else self._copy_attachments_to_product_template()
        return res


class ProductDocument(models.Model):
    _inherit = 'product.document'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Différer pour éviter les problèmes de récursion
        self.env.context = dict(self.env.context, sync_from_document=True)
        records.with_delay()._sync_to_bom_products() if hasattr(records, 'with_delay') else records._sync_to_bom_products()
        return records

    def write(self, vals):
        res = super().write(vals)
        # Éviter la récursion infinie
        if not self.env.context.get('sync_from_document'):
            self.env.context = dict(self.env.context, sync_from_document=True)
            self.with_delay()._sync_to_bom_products() if hasattr(self, 'with_delay') else self._sync_to_bom_products()
        return res

    def unlink(self):
        """Gérer la suppression de product.document"""
        for doc in self:
            if doc.ir_attachment_id:
                # Déclencher la gestion de suppression avant de supprimer
                doc.ir_attachment_id._handle_component_document_deletion()
        return super().unlink()

    def _sync_to_bom_products(self):
        """Synchronise les documents modifiés vers tous les produits finis qui utilisent ce composant"""
        for doc in self:
            att = doc.ir_attachment_id
            if not att:
                continue

            # Le document est lié à un produit
            if att.res_model in ['product.product', 'product.template']:
                if att.res_model == 'product.product':
                    product = self.env['product.product'].browse(att.res_id)
                    if not product.exists():
                        continue
                    templates = product.product_tmpl_id
                else:
                    templates = self.env['product.template'].browse(att.res_id)
                    if not templates.exists():
                        continue

                _logger.info(f"Recherche des BoM utilisant {templates.name}")

                # Trouver toutes les BoM où ce produit est utilisé comme composant
                bom_lines = self.env['mrp.bom.line'].search([
                    ('product_id.product_tmpl_id', 'in', templates.ids)
                ])
                
                boms = bom_lines.mapped('bom_id')
                
                _logger.info(f"Trouvé {len(boms)} BoM à synchroniser")

                # Lancer la synchro pour chaque BoM
                for bom in boms:
                    try:
                        bom.with_context(sync_from_document=True)._copy_attachments_to_product_template()
                    except Exception as e:
                        _logger.error(f"Erreur synchronisation BoM {bom.id}: {e}")


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    def write(self, vals):
        """Déclencher la synchronisation quand un attachement est modifié"""
        res = super().write(vals)
        
        # Si c'est un attachement de produit et qu'on n'est pas déjà en train de synchroniser
        if not self.env.context.get('sync_from_document'):
            for attachment in self:
                if attachment.res_model in ['product.product', 'product.template']:
                    # Trouver le product.document associé
                    product_docs = self.env['product.document'].search([
                        ('ir_attachment_id', '=', attachment.id)
                    ])
                    if product_docs:
                        product_docs._sync_to_bom_products()
        
        return res

    def unlink(self):
        """Gérer la suppression de documents composants"""
        for attachment in self:
            if attachment.res_model in ['product.product', 'product.template']:
                self._handle_component_document_deletion(attachment)
        
        return super().unlink()

    def _handle_component_document_deletion(self, attachment=None):
        """Gère la suppression d'un document de composant"""
        if not attachment:
            attachment = self
            
        # Trouver tous les produits finis qui ont ce document via une BoM
        if attachment.res_model == 'product.product':
            product = self.env['product.product'].browse(attachment.res_id)
            if not product.exists():
                return
            component_template = product.product_tmpl_id
        else:
            component_template = self.env['product.template'].browse(attachment.res_id)
            if not component_template.exists():
                return

        # Trouver les BoM qui utilisent ce composant
        bom_lines = self.env['mrp.bom.line'].search([
            ('product_id.product_tmpl_id', '=', component_template.id)
        ])
        
        boms = bom_lines.mapped('bom_id')
        
        for bom in boms:
            # Chercher les documents similaires dans le produit fini
            similar_attachments = self.search([
                ('res_model', '=', 'product.template'),
                ('res_id', '=', bom.product_tmpl_id.id),
                ('name', '=', attachment.name),
                ('checksum', '=', attachment.checksum),
            ])
            
            # Option 1: Marquage au lieu de suppression (RECOMMANDÉ)
            for similar_att in similar_attachments:
                # Ajouter un préfixe pour indiquer que le composant n'a plus ce document
                if not similar_att.name.startswith('[OBSOLETE]'):
                    similar_att.write({
                        'name': f'[OBSOLETE] {similar_att.name}',
                        'description': f'Document hérité du composant {component_template.name} (composant modifié le {fields.Datetime.now()})'
                    })
                    _logger.info(f"Document {similar_att.name} marqué comme OBSOLETE dans {bom.product_tmpl_id.name}")
            
            # Option 2: Suppression automatique (DÉCOMMENTEZ SI VOUS PRÉFÉREZ)
            # similar_attachments.unlink()
            
            _logger.info(f"Traitement de suppression document {attachment.name} pour BoM {bom.id}")