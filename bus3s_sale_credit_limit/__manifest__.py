# -*- coding: utf-8 -*-
{
    'name': 'Sales Credit',
    'author': 'bus3s.com',
    'website': 'https://www.bus3s.com',
    'support': 'o.allawy@bus3s.com',
    'version': '15.0.2',
    'category': 'Sales',
    'depends': [
        'sale_management',
    ],
    'data': [
        'data/sale_order_partner_credit_limit_group.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/sale_order_onhold.xml',
        'views/sale_customer_credit.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
