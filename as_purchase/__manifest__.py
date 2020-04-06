# -*- coding: utf-8 -*-
{
    'name': 'AhoraSoft Modulo de Compra',
    'version': '1.0.0',
    'category': 'purchase',
    'author': 'Ahorasoft',
    'summary': 'Customized purchase Management for Bolivia',
    'website': 'http://www.ahorasoft.com',
    'depends': [
         'base',
        'base_setup',
        'stock',
        'sale',
        'product',
        "purchase_stock",
        'purchase',
    ],
    'data': [
        'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/as_purchase.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}