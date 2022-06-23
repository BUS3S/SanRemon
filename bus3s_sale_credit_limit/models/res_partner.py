# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_credit = fields.Boolean('Set Customer Credit Limit ?')
    customer_credit_limit = fields.Float('Customer Credit Limit')
    set_customer_to_approve = fields.Boolean(
        'Set Customer To Approve  (Credit Limit Exceed)' , default=True )

    amount_due = fields.Monetary('Due Amount', compute='_compute_amount_due')

    @api.depends('credit', 'debit')
    def _compute_amount_due(self):
        for rec in self:
            rec.amount_due = rec.credit - rec.debit

