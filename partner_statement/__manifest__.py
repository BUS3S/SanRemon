{
    'name': 'Partner Statement Report',
    'version': '1.0',
    'author':'Omran Allawy',
    'category': 'Accounting & Finance',
    'summary': 'Statement Report',
    'description': 'Statement Report',
    'website': 'https://www.bus3s.com',
    'depends': ['account','base'],
    'data': [

             'wizard/partner_statement_wizard.xml',
             'report/partner_statement_report.xml',
             # 'report/custom_header_layout.xml',
             'security/ir.model.access.csv',
             ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
