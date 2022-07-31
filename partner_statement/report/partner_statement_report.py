from odoo import api, models,fields, _



class PartnerStatementRreport(models.AbstractModel):
    _name = 'report.partner_statement.partner_statement_report'
    _description ='Partner Account Statement Report'


    def _get_report_values(self, docids,data=None):
        report_obj = self.env.ref('partner_statement.action_report_partner_account_statement')
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        date = data['form']['date']
        account_type = data['form']['partner_account_type']
        if account_type == 'both':
            account_type = ['receivable','payable']
        else:
            account_type = [account_type]

        partner_id = data['form']['partner_id'][0]
        local_currency = data['form']['currency']
        journal_ids = data['form']['journal_ids']
        partner_obj = self.env['res.partner'].search([('id','=',partner_id)])

        od_sql_query = """
                        select sum(ml.debit)as debit,sum(ml.credit)as credit,sum(ml.balance)as balance,sum(ml.amount_currency)as amount_currency,ml.partner_id
                        From account_move_line as ml 
                        Left Join account_move as am on am.id = ml.move_id
                        Left Join account_account as aa on aa.id = ml.account_id
                        Where am.state = 'posted' and ml.partner_id = %s
                        and aa.internal_type in %s
                        and ml.date < %s
                        and am.journal_id in %s
                        and ml.debit>0
                        group by ml.partner_id
                """
        od_param = (partner_id,tuple(account_type),date_from,tuple(journal_ids),)
        self.env.cr.execute(od_sql_query, od_param)
        od_query_results = self.env.cr.dictfetchall()

        oc_sql_query = """
                            select sum(ml.debit)as debit,sum(ml.credit)as credit,sum(ml.balance)as balance,sum(ml.amount_currency)as amount_currency,ml.partner_id
                            From account_move_line as ml 
                            Left Join account_move as am on am.id = ml.move_id
                            Left Join account_account as aa on aa.id = ml.account_id
                            Where am.state = 'posted' and ml.partner_id = %s
                            and aa.internal_type in %s
                            and ml.date < %s
                            and am.journal_id in %s
                            and ml.credit>0
                            group by ml.partner_id
                        """
        oc_param = (partner_id, tuple(account_type), date_from, tuple(journal_ids),)
        self.env.cr.execute(oc_sql_query, oc_param)
        oc_query_results = self.env.cr.dictfetchall()


        sql_query = """
            Select  ml.date as date,ml.name as descr,ml.debit,ml.credit,ml.balance,ml.amount_currency,ml.company_currency_id,ml.currency_id,am.name
            From account_move_line as ml 
            Left Join account_move as am on am.id = ml.move_id
            Left Join account_account as aa on aa.id = ml.account_id
            Where am.state = 'posted' and ml.partner_id = %s
            and aa.internal_type in %s
            and ml.date between %s and %s
            and am.journal_id in %s
            order by ml.date
        """
        params = (partner_id,tuple(account_type),date_from,date_to,tuple(journal_ids),)
        self.env.cr.execute(sql_query, params)
        query_results = self.env.cr.dictfetchall()
        currency = dict()
        if local_currency:
            currency['code'] = self.env.user.company_id.currency_id.symbol
            currency['decimal'] = self.env.user.company_id.currency_id.decimal_places
        else:
            currency['code'] = partner_obj.property_purchase_currency_id.symbol
            currency['decimal'] = partner_obj.property_purchase_currency_id.decimal_places
        docargs = {
            'doc_ids': self._ids,
            'data':query_results,
            'local_currency':local_currency,
            'currency':currency,
            'od_open':od_query_results,
            'oc_open':oc_query_results,
            'date_from':date_from,
            'date_to':date_to,
            'partner':partner_obj.name,
            'partners':partner_obj.phone,

        }
        # return report_obj.render
        # {'partner_statement.partner_statement_report', }
        return {
            'doc_ids': self.ids,
            'doc_model': 'report.partner_statement.partner_statement_report',
            'docargs': docargs,
            'date_from': date_from,
            'date_to': date_to,
            'local_currency': local_currency,
            'currency': currency,
            'od_open': od_query_results,
            'oc_open': oc_query_results,
            'partner': partner_obj.name,
            'partners': partner_obj.phone,
            'data': query_results,
            'date': date,

        }