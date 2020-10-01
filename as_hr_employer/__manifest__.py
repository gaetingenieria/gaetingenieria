# -*- coding: utf-8 -*-
{
    'name': 'Ahorasoft Multiples Empleadores',
    'version': '1.0.4',
    'category': 'hr_contract',
    'author': 'Ahorasoft',
    'summary': 'Customized employer Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'hr',
        'base', 'hr_contract','hr_payroll'
    ],
    'data': [
        #'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/as_hr_employer.xml',
        'views/as_hr_contract.xml',
        'views/as_hr_employee.xml',
        'views/as_payslip_run.xml',
        'views/hr_payslip_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}