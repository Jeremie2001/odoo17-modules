# -*- coding: utf-8 -*-
# from odoo import http


# class MrpDocumentAuto(http.Controller):
#     @http.route('/mrp_document_auto/mrp_document_auto', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_document_auto/mrp_document_auto/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_document_auto.listing', {
#             'root': '/mrp_document_auto/mrp_document_auto',
#             'objects': http.request.env['mrp_document_auto.mrp_document_auto'].search([]),
#         })

#     @http.route('/mrp_document_auto/mrp_document_auto/objects/<model("mrp_document_auto.mrp_document_auto"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_document_auto.object', {
#             'object': obj
#         })

