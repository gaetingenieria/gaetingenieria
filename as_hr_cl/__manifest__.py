{
    'name': 'Chilean Payroll & Human Resources',
    'author': 'Ahorasoft',
    'website': 'http://www.ahorasoft.com',
    'license': 'AGPL-3',
    'depends': [
            'hr_payroll','hr_payroll_account','hr_contract','report_xlsx','hr','hr_holidays','hr_contract_types','report_xlsx'
            ,'as_hr_employer'],
    'license': 'AGPL-3',
    'version': '1.1.0',
    'description': """
Chilean Payroll & Human Resources.
==================================
    -Payroll configuration for Chile localization.
    -All contributions rules for Chile payslip.
    * Employee Basic Info
    * Employee Contracts
    * Attendance, Holidays and Sick Licence
    * Employee PaySlip
    * Allowances / Deductions / Company Inputs
    * Extra Time
    * Pention Chilean Indicators
    * Payroll Books
    * Previred Plain Text
    , ...
    Report
  """,
    'category': 'Localization/Chile',
    'data': [
        'views/menu_root.xml',
        'views/hr_indicadores_previsionales_view.xml',
        'views/hr_salary_rule_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_employee.xml',
        'views/hr_payslip_view.xml',
        'views/as_excel_txt.xml',
        'views/hr_afp_view.xml',
        'views/hr_payslip_run_view.xml',
        'views/as_res_partner.xml',
        'views/report_hrsalarybymonth.xml',
        'views/hr_salary_books.xml',
        'views/as_resource_calendar.xml',
        'views/hr_holiday_views.xml',
        'views/as_company.xml',
        'views/as_contract_type.xml',
        'report/as_hr_carta_preaviso.xml',
        'report/as_hr_carta_finiquito.xml',
        'report/as_anexo_contrato.xml',
        'wizard/as_carta_preaviso.xml',
        'wizard/as_carta_finiquito.xml',
        'views/wizard_export_csv_previred_view.xml',
        'wizard/as_planilla_sueldos.xml',
        'data/hr_salary_rule_category.xml',
        'data/hr_centros_costos.xml',
        'data/l10n_cl_hr_indicadores.xml',
        'data/l10n_cl_hr_isapre.xml',
        'data/l10n_cl_hr_afp.xml',
        'data/l10n_cl_hr_mutual.xml',
        'data/l10n_cl_hr_apv.xml',
        'data/hr_type_employee.xml',
        'data/resource_calendar_attendance.xml',
        'data/l10n_cl_hr_move_employee.xml',
        'data/hr_holidays_status.xml',
        'data/hr_contract_type.xml',
        'data/l10n_cl_hr_ccaf.xml',
        'data/account_journal.xml',
        'data/partner.xml',
        'data/l10n_cl_hr_payroll_data.xml',
        'security/ir.model.access.csv',
        'views/report_payslip.xml',
        'views/as_articulo_codigo.xml',
        'views/report/as_he_contrat_print.xml',
        'views/as_hr_employer.xml',
        'views/hr_move_employee.xml',
        'wizard/as_sii_1887.xml',
    ],
    'demo': ['demo/l10n_cl_hr_payroll_demo.xml'],
    'installable': True,
    'application': True,
    'auto_install': False
}
