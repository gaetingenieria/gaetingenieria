from pytz import timezone
from datetime import date, datetime, time

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'
    
    indicadores_id = fields.Many2one('hr.indicadores', string='Indicadores',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Defines Previred Forecast Indicators')
    movimientos_personal = fields.Many2many('hr.move.employee',  string="Código Movimiento")
    as_sin_movimiento = fields.Boolean( string="Código Movimiento S/n", default=False)
    as_days_rest = fields.Integer( string="dias a Descontar", default=False)
    # movimientos_personal = fields.Selection((('0', 'Sin Movimiento en el Mes'),
    #  ('1', 'Contratación a plazo indefinido'),
    #  ('2', 'Retiro'),
    #  ('3', 'Subsidios (L Médicas)'),
    #  ('4', 'Permiso Sin Goce de Sueldos'),
    #  ('5', 'Incorporación en el Lugar de Trabajo'),
    #  ('6', 'Accidentes del Trabajo'),
    #  ('7', 'Contratación a plazo fijo'),
    #  ('8', 'Cambio Contrato plazo fijo a plazo indefinido'),
    #  ('11', 'Otros Movimientos (Ausentismos)'),
    #  ('12', 'Reliquidación, Premio, Bono')     
    #  ), 'Código Movimiento', default="0")

    @api.onchange('date_start_mp','date_end_mp')
    def _get_type_days(self):
        dias = 0
        if self.date_start_mp and self.date_end_mp:
            dias = self.date_start_mp - self.date_end_mp
            dias=dias.days
        self.as_days_rest = dias

    @api.onchange('movimientos_personal')
    def _get_type_move(self):
        bandera = False
        for move in self.movimientos_personal:
            if move.codigo != '0':
                bandera = True
        self.as_sin_movimiento = bandera
    
    def _get_slip_patronales(self):
        line_slips = []
        for slip in self:
            for line in slip.line_ids:
                if line.category_id.code == 'COMP':
                    line_slips.append(line.id)
            if line_slips != []:
                return [('id', 'in',line_slips)]
        return []


    def _get_slip_no_patronales(self):
        line_slips = []
        for slip in self:
            for line in slip.line_ids:
                if line.category_id.code != 'COMP':
                    line_slips.append(line.id)
            if line_slips != []:
                return [('id', 'in',line_slips)]
        return []

    date_start_mp = fields.Date('Fecha Inicio MP',  help="Fecha de inicio del movimiento de personal")
    date_end_mp = fields.Date('Fecha Fin MP',  help="Fecha del fin del movimiento de personal")
    as_days = fields.Float(compute='_compute_other_net',string='Dias Trabajados')
    as_ingresos = fields.Monetary(compute='_compute_other_net',string='Ingresos')
    as_egresos = fields.Monetary(compute='_compute_other_net',string='Egresos')
    line_ids2 = fields.One2many('hr.payslip.line', 'slip_id', string='Aportes Patronales', readonly=True, domain=_get_slip_patronales)
    line_ids1 = fields.One2many('hr.payslip.line', 'slip_id', string='Payslip Lines', readonly=True,domain=_get_slip_no_patronales)
        

    def _compute_other_net(self):
        for payslip in self:
            payslip.as_days = payslip._get_worke_total('WORK100')
            payslip.as_ingresos = payslip._get_salary_line_total('HAB')
            payslip.as_egresos = payslip._get_salary_line_total('TDE')

    def _get_worke_total(self, code):
        lines = self.worked_days_line_ids.filtered(lambda line: line.code == code)
        return sum([line.number_of_days for line in lines])

    def get_slip_employee(self):
        return {
            'name': _('Nomina de Empleado'+str(self.employee_id.name)),
            'view_mode': 'form',
            'res_model': 'hr.payslip',
            'views': [(self.env.ref('hr_payroll.view_hr_payslip_form').id, 'form'), (False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': dict(self._context, create=False),
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if 'indicadores_id' in self.env.context:
            vals['indicadores_id'] = self.env.context.get('indicadores_id')
        if 'movimientos_personal' in self.env.context:
            vals['movimientos_personal'] = self.env.context.get('movimientos_personal')
        if 'payslip_run_id' in self.env.context:
            vals['date_to']= self.payslip_run_id.date_start
            vals['date_from']= self.payslip_run_id.date_end
        return super(HrPayslip, self).create(vals)

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contracts, date_from, date_to)
        temp = 0 
        dias = 0
        attendances = {}
        leaves = []
        for line in res:
            if line.get('code') == 'WORK100':
                attendances = line
            else:
                leaves.append(line)
        for leave in leaves:
            temp += leave.get('number_of_days') or 0
        #Dias laborados reales para calcular la semana corrida
        effective = attendances.copy()
        effective.update({
            'name': _("Dias de trabajo efectivos"),
            'sequence': 2,
            'code': 'EFF100',
        })
        # En el caso de que se trabajen menos de 5 días tomaremos los dias trabajados en los demás casos 30 días - las faltas
        # Estos casos siempre se podrán modificar manualmente directamente en la nomina.
        # Originalmente este dato se toma dependiendo de los dias del mes y no de 30 dias
        # TODO debemos saltar las vacaciones, es decir, las vacaciones no descuentan dias de trabajo. 
        if (effective.get('number_of_days') or 0) < 5:
            dias = effective.get('number_of_days')
        else:
            dias = 30 - temp
        attendances['number_of_days'] = dias
        res = []
        res.append(attendances)
        res.append(effective)
        res.extend(leaves)
        return res

    def get_date_employee(self,fecha):
        fecha_def = ''
        if fecha:
            dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
            mes = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m')
            ano = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
            fecha_def = str(dia)+'/'+ str(mes)+'/'+str(ano)
        return fecha_def