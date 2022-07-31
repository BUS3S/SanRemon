# -*- coding: utf-8 -*-
# from odoo import http


# class FreeOffCharge(http.Controller):
#     @http.route('/free_off_charge/free_off_charge', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/free_off_charge/free_off_charge/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('free_off_charge.listing', {
#             'root': '/free_off_charge/free_off_charge',
#             'objects': http.request.env['free_off_charge.free_off_charge'].search([]),
#         })

#     @http.route('/free_off_charge/free_off_charge/objects/<model("free_off_charge.free_off_charge"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('free_off_charge.object', {
#             'object': obj
#         })
