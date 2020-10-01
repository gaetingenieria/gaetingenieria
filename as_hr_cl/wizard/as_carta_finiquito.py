# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from pytz import timezone
from datetime import date, datetime, time
import logging
import base64
_logger = logging.getLogger(__name__)

class AhorasoftplanillaSueldos(models.TransientModel):
    _name = "as.carta.finiquito"
    _description = "Report payslip Report AhoraSoft"

    @api.onchange('partner_id')
    def _get_employer_id(self):    
        return {'domain':{'employer_id': [('id','in', tuple(self.partner_id.employer_ids.ids))]}}

    @api.onchange('employer_id')
    def _get_contract_id(self):    
        typs=[]
        domain = {}
        typep = self.env['hr.contract'].sudo().search([('employee_id', '=', self.partner_id.id),('employer_id', '=', self.employer_id.id)])
        for tipo in typep:
            typs.append(tipo.id)
        if typs !=[]:
            return {'domain':{'contract_id': [('id','in', tuple(typs))]}}
        else:
            return []

    partner_id = fields.Many2one('hr.employee', string="Empleado",required=True,domain="[('active', '=', True)]")
    contract_id = fields.Many2one('hr.contract', string="Contrato",required=True,domain=_get_contract_id)
    date = fields.Date('Fecha Retiro', default=fields.Date.context_today)
    dias = fields.Boolean('Carta de pre aviso')
    total = fields.Float('Indeminizacion Mutuo Acuerdo')
    as_anti_year = fields.Integer('Años')
    as_anti_mounth = fields.Integer('Meses')
    as_anti_days = fields.Integer('Dias')
    as_tiempo = fields.Integer('Tiempo de Trabajo')
    as_seguro = fields.Float('Valor de Seguro de sesantia')
    as_articulo_id = fields.Many2one('as.hr.articulo', string="Articulo y Código",required=True)
    employer_id = fields.Many2one('as.hr.employer', string='Empleador',domain=_get_employer_id)

    
    def export_pdf(self):
        self.ensure_one()
        context = self._context
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        data.update({'form': res})
        pdf = self.env.ref('as_hr_cl.as_hr_cl_carta_finiquito_report')
        modelo = 'hr.employee'
        content, content_type = self.env.ref('as_hr_cl.as_hr_cl_carta_finiquito_report').render_qweb_pdf(self, data=data)
        self.env['ir.attachment'].create({
            'name': self.partner_id.name and _("Carta finiquito %s.pdf") % self.partner_id.name or _("Carta finiquito.pdf"),
            'type': 'binary',
            'datas': base64.encodestring(content),
            'res_model': modelo,
            'res_id': self.partner_id.id,
        })
        return self.env.ref('as_hr_cl.as_hr_cl_carta_finiquito_report').report_action(self, data=data)

    @api.onchange('contract_id','date')
    def _compute_contract_id(self):
        Contract = self.env['hr.contract']
        for employee in self.contract_id:
            if employee.date_start:
                tiempo = self.date - employee.date_start
                self.as_anti_mounth = int((tiempo.days/30/12 - int(tiempo.days/30/12))*12)
                self.as_anti_days = int((tiempo.days/30/12 - int(tiempo.days/30/12))*30)
                if int(tiempo.days/30/12) >= 1:
                    self.as_anti_year = int(tiempo.days/30/12)
                else:
                    self.as_anti_year = 0
