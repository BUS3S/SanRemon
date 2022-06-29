# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions


class Partner(models.Model):
    _inherit = "res.partner"

    foc_percentage = fields.Float(string='FOC Percentage (%)', digits='FOC Percentage', default=0.0)
    foc_partner_id = fields.One2many('foc.sale.order', 'partner_ids', 'Partner')


class FocSaleOrder(models.Model):
    _name = "foc.sale.order"
    name = fields.Char(string='Order Reference', required=True)
    sale_order_ids = fields.Many2one(
        'sale.order', string='Sales Order', readonly=True,
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    partner_ids = fields.Many2one('res.partner', string='Partner')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    is_foc_applied = fields.Boolean('Is FOC Applied', default=False, store=True, readonly=False)

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])

        if vals.get('sale_order_ids'):
            sales_order = self.env['sale.order'].search([('id', '=', vals['sale_order_ids'])])
            vals['name'] = sales_order.name
        result = super(FocSaleOrder, self).create(vals)
        return result

    def name_get(self):
        if self._context.get('sale_show_partner_name'):
            res = []
            for order in self:
                name = order.name
                if order.partner_ids.name:
                    name = '%s - %s' % (name, order.partner_ids.name)
                res.append((order.id, name))
            return res
        return super(FocSaleOrder, self).name_get()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):

        result = super(SaleOrder, self).create(vals)
        create_rec = None
        if 'invoice_type' in vals and vals['invoice_type']:
            if vals['invoice_type'] == "foc" and vals['foc_type'] == 'foc_sales':
                if result.amount_total > result.foc_free_amount:
                    raise exceptions.ValidationError("Not Allowed to make total sales order more than FOC total")
                else:
                    for row in result.order_line:
                        row['discount'] = 100
            if vals['invoice_type'] == "foc" and vals['foc_type'] == 'samples':
                for row in result.order_line:
                    row['discount'] = 100
        foc_sales_order = self.env['foc.sale.order'].search([('sale_order_ids', '=', result.id)])
        if foc_sales_order:
            print("yes")
        else:
            create_rec = self.env['foc.sale.order'].create({
                'sale_order_ids': result.id,
                'partner_ids': vals['partner_id']
            })

        return result

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if self.invoice_type:
            if self.invoice_type == "foc" and self.foc_type == 'foc_sales' and self.state in ['draft']:
                print(self.amount_total, self.foc_free_amount)
                if self.amount_total > self.foc_free_amount:
                    raise exceptions.ValidationError("Not Allowed to make total sales order more than FOC total")
                else:
                    for row in self.order_line:
                        row['discount'] = 100
            if self['invoice_type'] == "foc" and self['foc_type'] == 'samples':
                for row in self.order_line:
                    row['discount'] = 100
        return res

    @api.depends('foc_sale_order_ids', 'foc_customer_percentage')
    def _amount_foc_all(self):
        """
        Compute the total amounts of the SO.
        """
        foc_orders_amount = 0
        foc_free_amount = 0
        for order in self:
            if order.foc_sale_order_ids:
                for row in order.foc_sale_order_ids:
                    foc_orders_amount += row._origin.sale_order_ids.amount_total
            foc_free_amount = (order.foc_customer_percentage / 100) * foc_orders_amount
            order.update({
                'foc_orders_amount': foc_orders_amount,
                'foc_free_amount': foc_free_amount
            })

    def action_confirm(self):
        vals = super().action_confirm()
        print(vals)
        for order in self:
            foc_sales_order = order.foc_sale_order_ids
            if foc_sales_order:
                for row in foc_sales_order:
                    row['is_foc_applied'] = 1
                    order_sa = row['sale_order_ids']
                    print(order_sa)
                    # order_sa.is_foc_applied = 1
                    self.env.cr.execute("""
                                UPDATE sale_order AS x
                                SET is_foc_applied = true                       
                                WHERE x.id = %s
                            """ % (order_sa.id)
                                        )
            # order.write({
            #     "delivery_status": "done"
            # })

    foc_sale_order_ids = fields.Many2many('foc.sale.order', string='FOC Sales Order',
                                          domain="[('partner_ids', '=', partner_id) ,('is_foc_applied','=', False)]")

    invoice_type = fields.Selection([
        ('cash', 'Cash'),
        ('credit', 'Credit'),
        ('foc', 'FOC'),
        ('return', 'Return')
    ], required=True)

    foc_type = fields.Selection([
        ('samples', 'Samples'),
        ('foc_sales', 'FOC Sales')
    ])
    is_foc_applied = fields.Boolean('Is FOC Applied', default=False, store=True, readonly=False)

    foc_orders_amount = fields.Float(string='FOC Orders Amount', digits='FOC Orders Amount', default=0.0, readonly=True,
                                     compute='_amount_foc_all')
    foc_customer_percentage = fields.Float(string='FOC Percentage', digits='FOC Percentage',
                                           related='partner_id.foc_percentage', readonly=True)
    foc_free_amount = fields.Float(string='FOC Free Amount', digits='FOC Free Amount', default=0.0, readonly=True,
                                   compute='_amount_foc_all')
