# -*- coding: utf-8 -*-
from odoo import api, models, fields,_
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportTax(models.AbstractModel):
    _name = 'report.as_hr_cl.carta_preaviso'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'info': self.info_sucursal(),
            'fechas': self.get_date_employee(data['form']['date']),
            'fechaend': self.get_date_employee(data['form']['date_end']),
            'mes': self.get_mes(fields.Datetime.now().strftime('%m')),
            'employee': self.get_employee(data['form']['partner_id'][0]),
            'articulo': self.get_model_inciso(data['form']['as_articulo_id'][0]),
            'fundamento': data['form']['as_fundamento'],
            'company': self.env.user.company_id,
            'employer': self.get_employer(data['form']['employer_id'][0]),
        }

    def get_model_inciso(self,model_id):
        model = self.env['as.hr.articulo'].sudo().search([('id', '=', model_id)],limit=1)
        return model    
    
    def get_employer(self,model_id):
        model = self.env['as.hr.employer'].sudo().search([('id', '=', model_id)],limit=1)
        return model


    def get_date_employee(self,fecha):
        dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
        mes = self.get_mes(datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m'))
        ano = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
        return ' '+str(dia)+' de '+ str(mes)+' de '+str(ano)+' '

    def get_employee(self,employee_id):
        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)],limit=1)
        return employee    
    
    def info_sucursal(self):
        info = ''
        diccionario_dosificacion= {}
        diccionario_dosificacion = {
            'nombre_empresa' : self.env.user.company_id.name or '',
            'nit' : self.env.user.company_id.vat or '',
            'direccion1' : self.env.user.company_id.street or '',
            'telefono' : self.env.user.company_id.phone or '',
            'ciudad' : self.env.user.company_id.city or '',
            'sucursal' : self.env.user.company_id.city or '',
            'pais' : self.env.user.company_id.country_id.name or '',
            'actividad' :  self.env.user.company_id.name or '',
            'fechal' : self.env.user.company_id.phone or '',
            'email' : self.env.user.company_id.email or '',


        }
        return diccionario_dosificacion

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