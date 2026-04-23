from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    intercompany_origin_id = fields.Many2one(
        'sale.order',
        string='Devis d\'origine',
        readonly=True,
        help='Devis source ayant généré cette copie inter-sociétés',
    )
    intercompany_copy_ids = fields.One2many(
        'sale.order',
        'intercompany_origin_id',
        string='Copies inter-sociétés',
    )
    intercompany_copy_count = fields.Integer(
        string='Nombre de copies',
        compute='_compute_intercompany_copy_count',
    )

    def _compute_intercompany_copy_count(self):
        for order in self:
            order.intercompany_copy_count = len(order.intercompany_copy_ids)

    def action_open_intercompany_copies(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Copies inter-sociétés',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.intercompany_copy_ids.ids)],
            'context': {'active_test': False},
        }
