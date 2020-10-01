from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime
class hr_contract(models.Model):
    _name = 'hr.employee.rules'
    _description = 'Employee rules slip'

    def _get_line_control(self):
        ids = []
        for employee in self.employee_ids:
            payslip = self.env['hr.payslip'].search([('state', '=', 'done'),('employee_id', '=', employee.id)])
            for line in payslip.line_ids:
                if line.code == self.codigo:
                    ids.append(line.id)
        self.line_ids = ids
        for employee in self.control_ids:
            cantidad = 0
            for line in self.line_ids:
                if line.employee_id == employee.employee_id:
                    cantidad += 1
            employee.qty= cantidad

            
        
    state = fields.Selection([('draft', 'Draft'),('active','Active'), ('closed','Closed')],string="State",readonly=True,default='draft')
    salary_rule_id = fields.Many2many('hr.salary.rule', string='Rule', readonly=True)
    type_employee = fields.Selection([('especifico', 'Especificos'),('todos','Todos')],string="Aplicar a ",default='especifico')
    employee_ids = fields.Many2many('hr.employee', string='Empleados', required=True)
    amount = fields.Float(string='Monto',default=1000)
    qty = fields.Integer(string='Cantidad',default=5)
    type_distr = fields.Selection([('fijo', 'Monto Fijo'),('prorrateo','Prorrateo')],string="Tipo distribución", default='fijo')
    start_date = fields.Date(string='Fecha Inicio')
    end_date = fields.Date(string='Fecha Fin',reaonly=True, store=True)
    name = fields.Char(string='Nombre de la regla')
    codigo = fields.Char(string='Codigo')
    line_ids = fields.Many2many('hr.payslip.line', string='Nominas', readonly=True,compute='_get_line_control')
    category_id = fields.Many2one('hr.salary.rule.category', string='Category', required=True)
    struct_ids = fields.Many2many('hr.payroll.structure', string='Avaibility in Structure',required=True)
    control_ids = fields.One2many('hr.rule.control', 'rules_id',string='Avaibility in Structure')
    employer_id = fields.Many2one('as.hr.employer', string='Empleador')
    
    @api.onchange('qty','start_date')
    def get_employee_date(self):    
        if self.start_date:
            self.end_date = (datetime.strptime(str(self.start_date), '%Y-%m-%d') + relativedelta(months=+int(self.qty))).strftime('%Y-%m-%d')
        
    @api.onchange('type_employee')
    def get_employee(self):
        for rule in self:
            if rule.type_employee == 'especifico':
                rule.employee_ids = self.env['hr.employee'].ids
            else:
                employee_ids = self.env['hr.employee'].search([('contract_id.state', '=', 'open')])
                rule.employee_ids = employee_ids.ids

    @api.model
    def create(self, vals):
        res = super(hr_contract, self).create(vals)  
        #se crea la regla solicitada
        restriccion =''
        #restriccion de si esta en el empleado
        inicio=''
        if res.employer_id:
            inicio +="""employer = False\n"""
        if res.start_date:
            inicio +="""inicio = False\n"""
        if res.end_date:
            inicio +="""fin = False\n"""        
        if res.qty > 0:
            inicio +="""cantidad = False\n"""
        restriccion = inicio+"""contiene = False\nfor line in employee.salary_rule_id:\n    if line.codigo == '"""+str(res.codigo)+"""':\n        contiene= True\n"""
        #restriccion de fecha
        result= """result = contiene"""
        if res.employer_id:
            restriccion += '        if payslip.employer_id.id == '+str(res.employer_id.id)+':\n            employer= True\n'
            result += """ and employer"""
        if res.start_date:
            restriccion += '        if payslip.date_from >= line.start_date:\n            inicio= True\n'
            result += """ and inicio"""
        if res.end_date:
            restriccion += '        if payslip.date_to <= line.end_date:\n            fin= True\n'
            result += """ and fin"""
        if res.qty > 0:
            restriccion += 'for lines in employee.salary_rule_id.control_ids:\n     if lines.employee_id== employee and lines.qty < lines.qty_rule:\n            cantidad= True\n'
            result += """ and cantidad"""
        restriccion +=result
        computo = """contiene = False\nfor line in employee.salary_rule_id:\n    if line.codigo == '"""+str(res.codigo)+"""':\n        contiene= line\nmonto = 0.0\nif contiene:\n    if contiene.type_distr == 'prorrateo' and contiene.qty > 0:\n        monto = contiene.amount/contiene.qty\n    else:\n        monto = contiene.amount\nresult = monto
        """
        vals = {
                'name': res.name,
                'code': res.codigo,
                'date_start': res.start_date,
                'date_end': res.end_date,
                'category_id': res.category_id.id,
                'condition_select': 'python',
                'condition_python': restriccion,
                'quantity': res.qty,
                'amount_fix': res.amount,
                'amount_select': 'code',
                'amount_python_compute': computo,
            }
        for struct in res.struct_ids:
            vals['struct_id'] = struct.id
            res.salary_rule_id = self.env['hr.salary.rule'].create(vals).ids
        for employee in res.employee_ids:
            self.env['hr.rule.control'].create({
                'rules_id' : res.id,
                'employee_id' : employee.id,
                'qty' : 0,
                'salary_rule_id' : res.salary_rule_id.id 
            })
            
        return res

    def action_confirm(self):
        for employee in self.employee_ids:
            rulesv = []
            for rules in employee.salary_rule_id:
                rulesv.append(rules.id)
            rulesv.append(self.id)
            employee.salary_rule_id = rulesv
        self.update({'state':'active'})

    def action_cancel(self):
        for employee in self.employee_ids:
            if employee.salary_rule_id == self.id:
                employee.salary_rule_id.unlink()
        for rule in self.salary_rule_id:
            rule.unlink()
        self.update({'state':'closed'})


class HrEmployee(models.Model):
    _name = 'hr.rule.control'
    _description = 'control de pagos'

    rules_id = fields.Many2one('hr.employee.rules', string='Empleados')
    employee_id = fields.Many2one('hr.employee', string='Empleados', required=True)
    qty = fields.Integer(string='Cantidad',default=0)
    qty_rule = fields.Integer(string='Cantidad regla',related='rules_id.qty')
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule', readonly=True)