from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from time import mktime
from odoo.exceptions import UserError, RedirectWarning, ValidationError, MissingError
import time
import calendar
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from datetime import datetime, timedelta

class hr_payslip_run(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'

    indicadores_id = fields.Many2one('hr.indicadores', 'Indicadores', states={'draft': [('readonly', False)]}, readonly=True, required=True)
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
    #  ), 'Movimientos Personal', default="0")
    movimientos_personal = fields.Many2many('hr.move.employee',  string="Código Movimiento")
    move_id = fields.Many2one('account.move', 'Movimiento Contable',compute='_compute_move_run')

    @api.model
    def create(self, vals):
        if 'slip_ids' in vals:
            for slip in vals['slip_ids']:
                slip[2]['date_to']= vals['date_end']
                slip[2]['date_from']= vals['date_start']
        return super(hr_payslip_run, self).create(vals)    
    
    def write(self, vals):
        res= super(hr_payslip_run, self).write(vals)
        if 'date_start' in vals and 'date_end' in vals:
            if self.slip_ids:
                for slip in self.slip_ids:
                    slip.update({'date_to':vals['date_end'],'date_from':vals['date_start']})
            mes1= (datetime.strptime(str(vals['date_end']), '%Y-%m-%d')).strftime('%m')
            year= (datetime.strptime(str(vals['date_end']), '%Y-%m-%d')).strftime('%Y')
            indicadores = self.env['hr.indicadores'].sudo().search([('month', '=', int(mes1)),('year', '=', int(year))],limit=1)
            mes_letra = self.get_mes(mes1)
            vals['name']= 'NOMINA DE '+mes_letra.upper()+' '+year
            vals['indicadores_id'] =indicadores.id
        return res

    @api.onchange('indicadores_id','date_start','date_end')
    def _get_value_nomina(self):
        for nomina in self:
            mes1= (datetime.strptime(str(nomina.date_start), '%Y-%m-%d')).strftime('%m')
            year= (datetime.strptime(str(nomina.date_start), '%Y-%m-%d')).strftime('%Y')
            indicadores = nomina.env['hr.indicadores'].sudo().search([('month', '=', int(mes1)),('year', '=', int(year))],limit=1)
            mes_letra = nomina.get_mes(mes1)
            nomina.name = 'NOMINA DE '+mes_letra.upper()+' '+year
            if indicadores:
                nomina.indicadores_id =indicadores.id    

    def _compute_move_run(self):
        for run in self:
            if run.slip_ids:
                run.move_id= run.slip_ids[0].move_id.id
            else:
                run.move_id= ()

    def get_mes(self,mes):
        mesesDic = {
            "01":'Enero',
            "02":'Febrero',
            "03":'Marzo',
            "04":'Abril',
            "05":'Mayo',
            "06":'Junio',
            "07":'Julio',
            "08":'Agosto',
            "09":'Septiembre',
            "10":'Octubre',
            "11":'Noviembre',
            "12":'Diciembre'
        }
        return mesesDic[str(mes)]
    

