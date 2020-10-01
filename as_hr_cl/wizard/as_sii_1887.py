# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class AhorasoftplanillaSueldos(models.TransientModel):
    _name = "as.sii.1887"
    _description = "Report payslip Report AhoraSoft"
    
    @api.onchange('employer_id')
    def _get_employer_id(self):  
        nominas = self.env['hr.payslip.run'].sudo().search([('employer_id', '=', self.employer_id.id)])  
        return {'domain':{'payslip_run_id': [('id','in', tuple(nominas.ids))]}}

    payslip_run_id = fields.Many2one('hr.payslip.run', string="Nomina",required=True,domain=_get_employer_id)
    as_filtro_dep = fields.Boolean( string="Agrupar por Departamento (PDF)")
    as_name_afp = fields.Many2many('hr.afp', string='Tipo de AFP')
    employer_id = fields.Many2one('as.hr.employer', string='Empleador')

    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.sii.1887'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('as_hr_cl.as_hr_cl_report_sii_1887_report').report_action(self, data=datas)
