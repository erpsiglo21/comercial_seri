# -*- coding: utf-8 -*-
{
    "name": "Sale Upload XML",
    'version': '1.0',
    'category': 'sale',
    'author':  'ERP Siglo 21',
    'website': 'https://erpsiglo21.cl',
    'license': 'AGPL-3',
    'description': "Generate sale order from XML file",
    'depends': [
            'l10n_cl_edi'
        ],
     'external_dependencies': {
         'python': [
             'xmltodict',
             'base64',
    #         'dicttoxml',
    #         'pdf417gen',
    #         'hashlib',
    #         'cchardet',
    #         'suds',#use suds-py3
    #         'urllib3',
    #         'signxml',
    #         'ast',
    #         'pysftp',
    #         'num2words',
    #         'xlsxwriter',
    #         'io',
         ]
     },
    'data': [
        'wizard/sale_upload_xml.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True
}
