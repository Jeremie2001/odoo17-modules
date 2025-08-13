from odoo import api, fields, models

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    projet = fields.Many2one(
        comodel_name='project.project',
        string="Projet",
        index=True,
        store=True,
        readonly=False,
    )

    # partner_number = fields.Char("N°", store=True, compute="compute_partner_number")
    partner_number = fields.Char(related='partner_id.numero_fournisseur')

    marge_global_percent = fields.Float("Marge Globale (%)", store=True)

    marge_global = fields.Monetary("Marge Globale", store=True, readonly=True, compute="_compute_marge_global")

    contact_client = fields.Char("Contact Client", store=True)
    contact_mlka = fields.Char("Contact MLKA", store=True)

    date_livraison = fields.Datetime("Date de livraison ", store=True)

    is_marge_global = fields.Boolean(
        string="Est-ce Global ?",
        default=False,
        required=True,
        store=True
    )

    # @api.depends("partner_id")
    # def compute_partner_number(self):
    #     for record in self:
    #         if record.partner_id:
    #             record.write({"partner_number": record.partner_id.numero_fournisseur})

    @api.depends("marge_global_percent", "order_line.marge_reduit", "order_line.discount")
    def _compute_marge_global(self):
        """Calcule la marge globale en fonction des marges des lignes de commande et des remises"""
        for record in self:
            global_discout = sum((line.price_subtotal if "Remise" in line.name else 0) for line in record.order_line if line.product_id)

            #Discount global
            if global_discout < 0:
                purchase_total = sum((line.purchase_price * line.product_uom_qty) for line in record.order_line if line.product_id and "Remise" not in line.name)
                record.marge_global = record.amount_untaxed - purchase_total if record.amount_untaxed else 0
                if not record.is_marge_global:
                    record.marge_global_percent = round(((record.marge_global/record.amount_untaxed)*100), 2) if record.amount_untaxed else 0
            else:
                record.marge_global = sum(line.marge_reduit for line in record.order_line if line.product_id)
                if not record.is_marge_global:
                    total = sum(line.price_subtotal for line in record.order_line if line.product_id)
                    record.marge_global_percent = round(((record.marge_global/total)*100), 2) if total else 0
            # if record.amount_untaxed:
            #     record.marge_global_percent = round(((record.marge_global/record.amount_untaxed)*100), 2)

    @api.onchange("marge_global_percent")
    def on_change_marge_percent(self):
        for record in self:
            if record.is_marge_global:
                record.marge_global = 0
                for line in record.order_line:
                    if line.product_id:
                        marge_pourcent = record.marge_global_percent/100
                        line.marge_percent_copy = marge_pourcent

                        line.onchange_margin_percent()
                        line._compute_margin()
                        line._onchange_marge_product()

