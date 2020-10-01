# -*- coding: utf-8 -*-
{
    'name': 'Ahorasoft Pago de Nominas',
    'version': '1.0.3',
    'category': 'hr',
    'author': 'Ahorasoft',
    'summary': 'Customized hr Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'hr',
        'base', 'account_payment','hr_payroll','account','as_hr_cl'
    ],
    'data': [
        'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/as_hr_slip.xml',
        'wizard/as_hr_payment.xml',
        'data/account_pago.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}