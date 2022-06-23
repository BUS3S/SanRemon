# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = "res.users"
    is_driver = fields.Boolean('Is Driver', default=False, store=True, readonly=False)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    driver_id = fields.Many2one(
        'res.users', string='Driver', index=True, tracking=2,
        domain="[('is_driver', '=', True)]", )

    def send_driver_message(self, driver_id, order, customer_name):
        check_u = self.env['res.users'].search([('id', '=', driver_id)])
        notification_ids = [(0, 0,
                             {
                                 'res_partner_id': check_u.partner_id.id,
                                 'notification_type': 'inbox'
                             }
                             )]
        subject = "Delivery Order"
        message = f"You are assigned to deliver order #{order} for {customer_name} customer"

        self.env['mail.message'].create({
            'message_type': "notification",
            'body': message,
            'subject': subject,
            'partner_ids': [(4, check_u.partner_id.id)],
            'model': self._name,
            'res_id': self.id,
            'notification_ids': notification_ids,
            'author_id': self.env.user.partner_id and self.env.user.partner_id.id
        })

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        if 'driver_id' in vals and vals['driver_id']:
            sales_order_driver = self.env['sales.orders.drivers'].search([('sales_order_id', '=', result.id)])
            if sales_order_driver:
                update_rec = sales_order_driver.write({
                    'driver_id': vals['driver_id']
                })
                self.send_driver_message(vals['driver_id'], result.name, result.partner_id.name)
            else:
                create_rec = self.env['sales.orders.drivers'].create({
                    'sales_order_id': result.id,
                    'driver_id': vals['driver_id']
                })
                self.send_driver_message(vals['driver_id'], result.name, result.partner_id.name)

        return result

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if 'driver_id' in values and values['driver_id']:
            if type(values['driver_id']) is not int:
                driver_id = values['driver_id'].id
            else:
                driver_id = values['driver_id']
            sales_order_driver = self.env['sales.orders.drivers'].search([('sales_order_id', '=', self.id)])
            if sales_order_driver:
                update_rec = sales_order_driver.write({
                    'driver_id': driver_id
                })
                self.send_driver_message(driver_id, self.name, self.partner_id.name)

            else:
                create_rec = self.env['sales.orders.drivers'].create({
                    'sales_order_id': self.id,
                    'driver_id': driver_id
                })
                self.send_driver_message(driver_id, self.name, self.partner_id.name)

        return res


class Picking(models.Model):
    _inherit = "stock.picking"

    driver_id = fields.Many2one(string='Driver', readonly=True, related='sale_id.driver_id', store=True)


class SalesOrderDriver(models.Model):
    _name = 'sales.orders.drivers'
    driver_id = fields.Many2one(
        'res.users', string='Driver', index=True, tracking=2,
        domain="[('is_driver', '=', True)]", )
    sales_order_id = fields.Many2one('sale.order', string='Sales Order')
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Delivered')
    ], string='Delivery Status', readonly=True, copy=False, index=True, tracking=3, default='pending')

    def name_get(self):
        res = []
        for order in self:
            new_name = order.driver_id.name + ' _ ' + order.sales_order_id.name
            name = '%s' % new_name
            res.append((order.id, name))

        return res

    def action_confirm(self):
        for order in self:
            order.write({
                "delivery_status": "done"
            })
