from odoo import models, fields, api


class project_quotation_link(models.Model):
    _inherit = 'project.project'

    entreprise = fields.Many2one(
    'res.partner',
    string="Entreprise",
    domain=[('is_company', '=', True)],
    required=True
    )

    description_projet = fields.Text(string = "Description du projet", required=True )

    responsable = fields.Many2one(
        'res.partner',
        string="Responsable",
        domain="[('parent_id', '=', entreprise), ('is_company', '=', False)]"
    )
    

    sale_order_ids = fields.Many2many(
        'sale.order',
        string="Devis associés",
        compute='_compute_sale_orders',
        store=False
    )
    
    sale_order_count = fields.Integer(
        string="Nombre de devis",
        compute='_compute_sale_orders'
    )

    

    def _compute_sale_orders(self):
        
        # Optimisation: une seule requête pour tous les projets
        if not self:
            return
        
        # Recherche groupée de tous les devis correspondants
        sale_orders = self.env['sale.order'].search([
            ('projet', 'in', self.ids)
        ])
        
        orders_by_project = {}
        for order in sale_orders:
            orders_by_project.setdefault(order.projet.id, []).append(order.id)
        
        # Assigner les valeurs en une passe
        for proj in self:
            order_ids = orders_by_project.get(proj.id, [])
            proj.update({
                'sale_order_ids': [(6, 0, order_ids)],
                'sale_order_count': len(order_ids)
            })


