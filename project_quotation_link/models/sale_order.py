

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    projet = fields.Many2one(
        comodel_name='project.project',
        string="Projet",
        index=True,
        store=True,
        readonly=False,
    )
