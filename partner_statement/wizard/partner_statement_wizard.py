from openerp import api, models,fields, _


class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'
    _description = 'Partner Account Statement Wizard'

    @api.model
    def default_get(self, default_fields):
        res = super(PartnerStatementWizard, self).default_get(default_fields)
        res.update({
            'journal_ids': [(4, x.id,) for x in self.env['account.journal'].search([])],
        })
        return res

    date_from = fields.Date('From',required=True)
    date_to = fields.Date('To',required=True)
    move_line_state = fields.Selection([('0','Only Posted Entries'),('1','All Entries')],default='0',string='Entry State')
    partner_account_type = fields.Selection([('receivable','Receivable Accounts'),('payable','Payable Accounts'),('both','Both')],default='both')
    partner_id = fields.Many2one('res.partner',string='Partner',required=True)
    currency = fields.Boolean('Local Currency',default=True)
    journal_ids = fields.Many2many(comodel_name='account.journal',string='Journals',required=True)
    date = fields.Date(string="Report Date",default=fields.Date.today, required=True)
    def view_report(self):
        data = {}
        data['form'] = {}
        data['form'].update(self.read(['partner_account_type','date_from','date_to','partner_id','move_line_state','currency','journal_ids','date'])[0])
        return self.env.ref('partner_statement.action_report_partner_account_statement').report_action(self,data)