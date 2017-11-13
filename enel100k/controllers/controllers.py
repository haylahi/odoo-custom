# -*- coding: utf-8 -*-
from odoo import http

# class Enel100k(http.Controller):
#     @http.route('/enel100k/enel100k/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/enel100k/enel100k/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('enel100k.listing', {
#             'root': '/enel100k/enel100k',
#             'objects': http.request.env['enel100k.enel100k'].search([]),
#         })

#     @http.route('/enel100k/enel100k/objects/<model("enel100k.enel100k"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('enel100k.object', {
#             'object': obj
#         })