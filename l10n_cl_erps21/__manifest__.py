# -*- coding: utf-8 -*-
{
    'name': "l10n_cl_erps21",

    'summary': """
        Adecuaciones y localizaciones de ERPS21 sobre odoo 14 enterprise
    """,

    'description': """
        Adecuaciones y localizaciones de ERPS21 sobre odoo 14 enterprise
    """,

    'author': "ERP Siglo 21",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['l10n_cl_edi'],

    # always loaded
    'data': [
        'report/account_report.xml',
        'views/account_move_views.xml',
        'views/report_invoice.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [
    ],
}
