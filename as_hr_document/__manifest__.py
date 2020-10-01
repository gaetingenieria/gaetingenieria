# -*- coding: utf-8 -*-
{
    'name': 'Ahorasoft Documentos Empleadores cuando expiran',
    'version': '1.0.1',
    'category': 'hr',
    'author': 'Ahorasoft',
    'summary': 'Customized document Management',
    'website': 'http://www.ahorasoft.com',
    'depends': ['base', 'hr','as_hr_employer'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_document_view.xml',
        'views/document_type_view.xml',
        'views/hr_document_template.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
