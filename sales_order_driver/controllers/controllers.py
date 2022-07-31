# -*- coding: utf-8 -*-
# from odoo import http


# class SalesOrderDriver(http.Controller):
#     @http.route('/sales_order_driver/sales_order_driver', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_order_driver/sales_order_driver/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_order_driver.listing', {
#             'root': '/sales_order_driver/sales_order_driver',
#             'objects': http.request.env['sales_order_driver.sales_order_driver'].search([]),
#         })

#     @http.route('/sales_order_driver/sales_order_driver/objects/<model("sales_order_driver.sales_order_driver"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_order_driver.object', {
#             'object': obj
#         })
