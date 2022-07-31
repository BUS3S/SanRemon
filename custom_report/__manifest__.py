# -*- coding: utf-8 -*-
{
    "name": "Custom Report",
    "version": "12.0.0.0.1",
    "summary": "",
    "description": """""",
    "category": "Sales/Sales",
    "author": '',
    "website": "",
    "company": "",
    'version': '1.0',
    'depends': ['sale', 'sale_management'],
    'data': [
        'report/sale_report.xml',
        'report/custom_header_layout.xml',
        'report/invoice_report_templates.xml',
        'report/purchase_order.xml',
        'data/paperformat.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
