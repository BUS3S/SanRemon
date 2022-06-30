# -*- coding: utf-8 -*-
{
    'name': "bus3s_Paci",



    'author': "Bussiness Sysmatic",
    'website': "https://www.bus3s.com",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
