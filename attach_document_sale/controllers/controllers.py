# -*- coding: utf-8 -*-
# from odoo import http


# class AttachDocumentSale(http.Controller):
#     @http.route('/attach_document_sale/attach_document_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attach_document_sale/attach_document_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('attach_document_sale.listing', {
#             'root': '/attach_document_sale/attach_document_sale',
#             'objects': http.request.env['attach_document_sale.attach_document_sale'].search([]),
#         })

#     @http.route('/attach_document_sale/attach_document_sale/objects/<model("attach_document_sale.attach_document_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attach_document_sale.object', {
#             'object': obj
#         })

