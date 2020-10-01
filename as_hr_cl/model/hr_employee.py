import re
import logging
from pytz import timezone
from datetime import date, datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from itertools import cycle
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    firstname = fields.Char("Firstname")
    last_name = fields.Char("Last Name")
    middle_name = fields.Char("Middle Name", help='Employees middle name')
    mothers_name = fields.Char("Mothers Name", help='Employees mothers name')
    type_id = fields.Many2one('hr.type.employee', 'Tipo de Empleado')
    formated_vat = fields.Char(translate=True, string='Printable VAT', store=True, help='Show formatted vat')
    as_fecha_ingreso = fields.Date(string='Fecha de Ingreso', default=fields.Date.context_today)
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", required=True,tracking=True,default=fields.Date.context_today)

    @api.model
    def _get_computed_name(self, last_name, firstname, last_name2=None, middle_name=None):
        names = []
        if firstname:
            names.append(firstname)
        if middle_name:
            names.append(middle_name)
        if last_name:
            names.append(last_name)
        if last_name2:
            names.append(last_name2)
        return " ".join(names)

    @api.onchange('firstname', 'mothers_name', 'middle_name', 'last_name')
    def get_name(self):
        if self.firstname and self.last_name:
            self.name = self._get_computed_name(self.last_name, self.firstname, self.mothers_name, self.middle_name)

    @api.onchange('identification_id')
    def onchange_document(self):
        identification_id = (
            re.sub('[^1234567890Kk]', '',
            str(self.identification_id))).zfill(9).upper()
        self.identification_id = '%s.%s.%s-%s' % (
            identification_id[0:2], identification_id[2:5], identification_id[5:8],
            identification_id[-1])
        self.validarRut(self.identification_id)

    def check_identification_id_cl(self, identification_id):
        body, vdig = '', ''
        if len(identification_id) > 9:
            identification_id = identification_id.replace('-','',1).replace('.','',2)
        if len(identification_id) != 9:
            raise UserError(u'El Rut no tiene formato')
        else:
            body, vdig = identification_id[:-1], identification_id[-1].upper()
        try:
            vali = range(2,8) + [2,3]
            operar = '0123456789K0'[11 - (
                sum([int(digit)*factor for digit, factor in zip(
                    body[::-1],vali)]) % 11)]
            if operar == vdig:
                return True
            else:
                raise UserError(u'El Rut no tiene formato')
        except IndexError:
            raise UserError(u'El Rut no tiene formato')

    def validarRut(self,rut):
        rut = rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        aux = rut[:-1]
        dv = rut[-1:]
    
        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11
    
        if str(res) == dv:
            return True
        elif dv=="K" and res==10:
            return True
        else:
            raise UserError(_("El Rut no tiene formato su terminal deberia ser %r.") %  str(res))

    @api.constrains('identification_id')
    def _rut_unique(self):
        for r in self:
            if not r.identification_id:
                continue
            employee = self.env['hr.employee'].search(
                [
                    ('identification_id', '=', r.identification_id),
                    ('id', '!=', r.id),
                ])
            if r.identification_id != "55.555.555-5" and employee:
                raise UserError(u'El Rut debe ser único')
