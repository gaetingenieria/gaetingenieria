# -*- coding: utf-8 -*-
{
    'name': 'Ahorasoft Reglas Especificas para Empleados',
    'version': '1.0.5',
    'category': 'hr_payroll',
    'author': 'Ahorasoft',
    'summary': 'Customized hr_payroll Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'hr',
        'base','hr_payroll','hr_contract','as_hr_employer'
    ],
    'data': [
        #'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/as_hr_rules_employee.xml',
        'views/as_hr_employee.xml',
        'data/data_email.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}