# -*- coding: utf-8 -*-
{
    'name': 'AhoraSoft Modulo de Inventario',
    'version': '1.0.0',
    'category': 'stock',
    'author': 'Ahorasoft',
    'summary': 'Customized Inventarios Management for Bolivia',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'base','product', 'stock','report_xlsx',
    ],
    'data': [
        #'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'wizard/as_kardex_productos_wiz.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}