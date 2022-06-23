{
    'name': "sales order driver",

    'summary': """
        Assign driver to sales orders""",

    'description': """
        Assign driver sales orders
    """,

    'author': "Business Sysmatic",
    'website': "https://bus3s.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_management'],

    # always loaded
    'data': [
        'security/driver_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/assign_driver_orders.xml',
        'views/sales_orders_driver_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-
