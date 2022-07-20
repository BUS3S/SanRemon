# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#   Aktiv Software:
#       - Harsh Mandaliya
#       - Geet Thakkar
#       - Harshil Soni


{
    'name': 'Return product of sale order',
    'summary': """This module will return sale order product.""",
    'version': '15.0.1.0.2',
    'description': """This module will return the sale order product""",
    'author': "Aktiv Software",
    'company': 'Aktiv Software',
    'website': "http://www.aktivsoftware.com",
    'category': 'Sales',
    'price': 15.00,
    'currency': "EUR",
    'depends': ['sale', 'sale_management', 'stock'],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'data/return_ir_sequence.xml',
        'views/return_order_line_views.xml',
        'views/res_config_settings_inherited.xml',
        'views/account_move_inherited.xml',
        'views/return_order_views.xml',
        'views/sale_order_views.xml',
    ],
    'demo': [],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
}
