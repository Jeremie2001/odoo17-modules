# -*- coding: utf-8 -*-
# from odoo import http


# class SaleIntercompanyCopy(http.Controller):
#     @http.route('/sale_intercompany_copy/sale_intercompany_copy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_intercompany_copy/sale_intercompany_copy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_intercompany_copy.listing', {
#             'root': '/sale_intercompany_copy/sale_intercompany_copy',
#             'objects': http.request.env['sale_intercompany_copy.sale_intercompany_copy'].search([]),
#         })

#     @http.route('/sale_intercompany_copy/sale_intercompany_copy/objects/<model("sale_intercompany_copy.sale_intercompany_copy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_intercompany_copy.object', {
#             'object': obj
#         })

