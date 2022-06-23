from odoo import api, fields, models, _, exceptions
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta
import decimal


class assign_driver_orders_wizard(models.TransientModel):
    _name = 'assign.driver.orders.wizard'
    _description = 'Assign Driver'

    driver_id = fields.Many2one(
        'res.users', string='Driver', index=True, tracking=2,
        domain="[('is_driver', '=', True)]", )

    def _get_default_company(self):
        if not self._context.get('active_model'):
            return
        orders = self.env[self._context['active_model']].browse(self._context['active_ids'])
        return orders

    def action_assign_driver(self):
        driver_id = self.driver_id if self.driver_id else None
        orders = self._get_default_company()
        if orders:
            for order in orders:
                if driver_id:
                    order.write({'driver_id': driver_id})
                    # sales_order_driver = self.env['sales.orders.drivers'].search([('sales_order_id', '=', order.id)])
                    # if sales_order_driver:
                    #     update_rec = sales_order_driver.write({
                    #         'driver_id': driver_id
                    #     })
                    #
                    # else:
                    #     create_rec = self.env['sales.orders.drivers'].create({
                    #         'sales_order_id': order.id,
                    #         'driver_id': driver_id
                    #     })
                    # order.send_driver_message(driver_id.id, order.name, order.partner_id.name)
