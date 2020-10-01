from odoo import api, fields, models, tools, _


class hr_salary_rule(models.Model):
    _inherit = 'hr.salary.rule'
    _description = 'Salary Rule'
    
    date_start = fields.Date('Fecha Inicio',  help="Fecha de inicio de la regla salarial")
    date_end = fields.Date('Fecha Fin',  help="Fecha del fin de la regla salarial")
    register_id = fields.Many2one('hr.contribution.register', string='Contribution Register', help="Eventual third party involved in the salary payment of the employees.")

class HrRuleInput(models.Model):
    _name = 'hr.rule.input'
    _description = 'Salary Rule Input'

    name = fields.Char(string='Description', required=True)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    input_id = fields.Many2one('hr.salary.rule', string='Salary Rule Input', required=True)
