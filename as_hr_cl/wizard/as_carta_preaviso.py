# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import logging
_logger = logging.getLogger(__name__)

class AhorasoftplanillaSueldos(models.TransientModel):
    _name = "as.carta.preaviso"
    _description = "Report payslip Report AhoraSoft"

    partner_id = fields.Many2one('hr.employee', string="Empleado",required=True,domain="[('active', '=', True)]")
    as_articulo_id = fields.Many2one('as.hr.articulo', string="Articulo y Código",required=True)
    as_fundamento = fields.Text(string='Fundamentos de carta', default="labores que usted realizaba dentro de la empresa, estaba vinculado a un servicio y cliente especifico, y dicho cliente prescindió de los servicios con nuestra empresa")
    date = fields.Date('Fecha Emisión', default=fields.Date.context_today)
    date_end = fields.Date('Fecha Retiro', default=fields.Date.context_today)
    employer_id = fields.Many2one('as.hr.employer', string='Empleador')

    def export_pdf(self):
        self.ensure_one()
        context = self._context
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        pdf = self.env.ref('as_hr_cl.as_hr_cl_carta_preaviso_report')
        modelo = 'hr.employee'
        content, content_type = self.env.ref('as_hr_cl.as_hr_cl_carta_preaviso_report').render_qweb_pdf(self, data=data)
        self.env['ir.attachment'].create({
            'name': self.partner_id.name and _("Carta preaviso %s.pdf") % self.partner_id.name or _("Carta preaviso.pdf"),
            'type': 'binary',
            'datas': base64.encodestring(content),
            'res_model': modelo,
            'res_id': self.partner_id.id,
        })
        return self.env.ref('as_hr_cl.as_hr_cl_carta_preaviso_report').report_action(self, data=data)
