# -*- coding: utf-8 -*-
{
    'name': 'AhoraSoft Modulo de Produccion',
    'version': '1.0.1',
    'category': 'mrp',
    'author': 'Ahorasoft',
    'summary': 'Customized mrp Management for Bolivia',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'mrp',
        'base','product', 'stock', 'resource'
    ],
    'data': [
        'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/as_mrp.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}