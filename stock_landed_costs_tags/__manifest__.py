# -*- coding: utf-8 -*-
{
    'name': 'Landed costs tags',
    'summary': 'Retrieves the bills on landed costs depending on analityc tags.',
    'version': '1.0.14',
    'author': 'ERP Siglo 21',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    'depends': [
        'stock_landed_costs'
    ],
    'data': [
        'data/res_config.xml',
        'data/res_users_data.xml',
        'views/stock_landed_cost_views.xml',
        'views/account_move_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
