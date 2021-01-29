# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Currency',
    'version': '1.0',
    'category': 'Sale',
    'license': 'AGPL-3',
    'summary': 'Converts the amount and currency in the sale order into the local currency',
    'author': u'ERP Siglo 21',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}