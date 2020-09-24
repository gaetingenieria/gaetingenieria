# -*- coding: utf-8 -*-
{
    'name' : "Ahorasoft customizaciones GAET",
    'version' : "1.0.0",
    'author'  : "Ahorasoft",
    'description': """
Customizaciones para GAET
===========================

Custom module for GAET
    """,
    'category' : "Sale",
    'depends' : [ "base",
        "sale_management",
        'product',"purchase",'sale','account_reports'],
    'website': 'http://www.ahorasoft.com',
    'data' : [
        'views/as_retencion.xml',
        'views/as_sale_order.xml',
        'views/as_report_format.xml',
        'views/as_medio_pago.xml',
        'views/as_account_move.xml',
        'views/as_sequence.xml',
        'views/as_payment_acquirer.xml',
        'views/as_account_payment.xml',
        'views/as_view_payment.xml',
        'views/report/as_sale_report_templates.xml',
        'wizard/as_report_sales.xml',
        'wizard/as_report_planilla_general.xml',
        'security/ir.model.access.csv',
     
             ],
    'demo' : [],
    'qweb': [],
    'installable': True,
    'auto_install': False
}
