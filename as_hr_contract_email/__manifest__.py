# -*- coding: utf-8 -*-
{
    'name': 'Ahorasoft Envio de Email sobre estatus de Contratos',
    'version': '1.0.0',
    'category': 'hr_contract',
    'author': 'Ahorasoft',
    'summary': 'Customized hr_contract Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'hr',
        'base','hr_contract','hr_payroll'
    ],
    'data': [
        # 'security/as_group_view.xml',
        # 'security/ir.model.access.csv',
        'views/as_res_config.xml',
        'data/data_email.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}