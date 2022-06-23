# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderPartnerCredit(models.TransientModel):
    _name = 'sale.order.partner.credit'
    _description = 'Sale Order Partner Credit'

    name = fields.Many2one("sale.order", "Sale Order", readonly=True)
    order_partner = fields.Many2one("res.partner", "Customer", readonly=True)
    customer_credit_limit = fields.Float(
        'Customer Credit Limit', readonly=True)
    set_customer_to_approve = fields.Boolean(
        'Customer To Approve (Credit Limit Exceed)')

    total_receivable = fields.Float("Total Receivable", readonly=True)
    current_order = fields.Float("Current Sale Order", readonly=True)
    sale_orders_cnt_amt = fields.Char("Sales Orders Pending", readonly=True)
    cust_invoice_cnt_amt = fields.Char(
        "Customer Invoice Pending", readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderPartnerCredit, self).default_get(fields)
        if self._context.get('active_id', False) and self._context.get('active_model', False) == 'sale.order':
            sale_obj = self.env['sale.order'].search(
                [('id', '=', self._context.get('active_id'))], limit=1)
            if sale_obj:
                res = {}
                so_pend = ''
                inv_pend = ''
                ord_cnt = 0
                ord_amt = 0
                inv_cnt = 0
                inv_amt = 0
                res.update({'name': sale_obj.id})
                res.update({'current_order': sale_obj.amount_total})
                if sale_obj.partner_id:
                    res.update({'order_partner': sale_obj.partner_id.id, 'set_customer_to_approve': sale_obj.partner_id.set_customer_to_approve,
                                'total_receivable': sale_obj.partner_id.credit, 'customer_credit_limit': sale_obj.partner_id.customer_credit_limit})
                so_pend_obj = self.env['sale.order'].search(
                    [('state', 'not in', ['done', 'cancel']), ('partner_id', '=', sale_obj.partner_id.id)])

                inv_pend_obj = self.env['account.move'].search([('move_type','=','out_invoice'),
                    ('payment_state','!=','paid'),('state','not in',['cancel']),('partner_id','=',sale_obj.partner_id.id )])

                for rec in so_pend_obj:
                    ord_cnt += 1
                    ord_amt += rec.amount_total
                if ord_cnt > 0:
                    so_pend = str(ord_cnt) + \
                        ' Sales Order(s) (Amt) : ' + str(ord_amt)
                    res.update({'sale_orders_cnt_amt': so_pend})
                for rec in inv_pend_obj:
                    inv_cnt += 1
                    inv_amt += rec.amount_total
                if inv_cnt > 0:
                    inv_pend = str(inv_cnt) + \
                        ' Invoice(s) (Amt) : ' + str(inv_amt)
                    res.update({'cust_invoice_cnt_amt': inv_pend})
        return res

    def to_approve_sale_order(self):
        if self and self.name and self.order_partner:

            partner_obj = self.env['res.partner'].search(
                [('id', '=', self.order_partner.id)], limit=1)
            partner_obj.write(
                {'set_customer_to_approve': self.set_customer_to_approve})

            sale_obj = self.env['sale.order'].search([('id','=',self.name.id)])
            sale_obj.write({ 'state' : 'to_approve' })

    def confirm_sale_order(self):
        if self and self.name and self.order_partner:

            partner_obj = self.env['res.partner'].search(
                [('id', '=', self.order_partner.id)], limit=1)
            partner_obj.write(
                {'set_customer_to_approve': self.set_customer_to_approve})

            sale_obj = self.env['sale.order'].search(
                [('id', '=', self.name.id)])
            sale_obj.write({'partner_credit_conform': True})

            sale_obj.action_confirm()

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_credit_conform = fields.Boolean("Confirm Partner Order on Credit")
    state = fields.Selection(selection_add=[('to_approve', 'TO Approve')])

    def action_to_approve_confirm(self):
        if self:
            self.action_confirm()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id and self.partner_id.set_customer_to_approve:
            warning_mess = {
                'message': ('Selected Customer is set On Hold due to its credit limit exceeds.'),
                'title': "Warning"
            }
            return {'warning': warning_mess}
        return res

    def action_confirm(self):  # Overwrite Existing
        # If Partner Credit Limit Group Permission
        if self.state == 'to_approve' and self.user_has_groups('bus3s_sale_credit_limit.sh_group_sale_order_partner_credit_limit'):
            res = super(SaleOrder, self).action_confirm()
            return res
        elif self and self.partner_id and self.partner_id.customer_credit:  # If Check
            tot_receivable = self.partner_id.credit + self.amount_total
            crdt_lmt = self.partner_id.customer_credit_limit
            if tot_receivable > crdt_lmt:
                if self.partner_credit_conform:  # Must Confirm Order at any condition
                    res = super(SaleOrder, self).action_confirm()
                    return res
                else:
                    return {
                        'name': 'Customer Credit',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'sale.order.partner.credit',
                        'view_id': self.env.ref('bus3s_sale_credit_limit.sale_order_partner_credit_limit_form').id,
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'context': self.env.context,
                    }
            else:
                res = super(SaleOrder, self).action_confirm()
                return res
        else:
            res = super(SaleOrder, self).action_confirm()
            return res

