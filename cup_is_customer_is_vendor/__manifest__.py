# -*- coding: utf-8 -*-
{
    'name': "Is a Customer and Is a Vendor",

    'summary': """
        Add Field Is a Customer And Is a Vendor""",


    'license': "LGPL-3",
    'author': "omran allawy",
    'website': "www.bus3s.com/",


    'version': '0.1',

    'depends': ['base','account','sale_management','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}