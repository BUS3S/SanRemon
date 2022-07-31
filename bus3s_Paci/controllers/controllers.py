# -*- coding: utf-8 -*-
# from odoo import http


# class Bus3sCrm(http.Controller):
#     @http.route('/bus3s_Paci/bus3s_Paci/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bus3s_Paci/bus3s_Paci/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bus3s_Paci.listing', {
#             'root': '/bus3s_Paci/bus3s_Paci',
#             'objects': http.request.env['bus3s_Paci.bus3s_Paci'].search([]),
#         })

#     @http.route('/bus3s_Paci/bus3s_Paci/objects/<model("bus3s_Paci.bus3s_Paci"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bus3s_Paci.object', {
#             'object': obj
#         })
