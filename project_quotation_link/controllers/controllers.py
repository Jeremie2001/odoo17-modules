# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectQuotationLink(http.Controller):
#     @http.route('/project_quotation_link/project_quotation_link', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_quotation_link/project_quotation_link/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_quotation_link.listing', {
#             'root': '/project_quotation_link/project_quotation_link',
#             'objects': http.request.env['project_quotation_link.project_quotation_link'].search([]),
#         })

#     @http.route('/project_quotation_link/project_quotation_link/objects/<model("project_quotation_link.project_quotation_link"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_quotation_link.object', {
#             'object': obj
#         })

