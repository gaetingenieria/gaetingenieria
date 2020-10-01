# -*- coding: utf-8 -*-
from odoo import api, models, fields,_
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportTax(models.AbstractModel):
    _name = 'report.as_hr_cl.anexo_contrato'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'info': self.info_sucursal(),
            'fecha_actual': self.get_date_actual(),
            'fecha_inicial': self.get_date_employee(data['form']['date_end']),
            'fecha_final': self.get_date_employee(data['form']['date_end']),
            'mes': self.get_mes(fields.Datetime.now().strftime('%m')),
            'employee': self.get_employee(data['form']['employee_id'][0]),
            'contract': self.get_contract(data['form']['id']),
            'marital': self.get_material(self.get_employee(data['form']['employee_id'][0]).marital),
            'company': self.env.user.company_id,
            'fecha_nacimiento' : self.get_date_employee(self.get_employee(data['form']['employee_id'][0]).birthday),
            'employer': self.get_employer(data['form']['employee_id'][0]),
        }

    def get_employer(self,model_id):
        model = self.env['as.hr.employer'].sudo().search([('id', '=', self.get_contract(model_id).employer_id.id)],limit=1)
        return model
        
    def get_model_inciso(self,model_id):
        model = self.env['as.hr.articulo'].sudo().search([('id', '=', model_id)],limit=1)
        return model

    def get_date_actual(self):
        dia = fields.Datetime.now().strftime('%d')
        mes = self.get_mes(fields.Datetime.now().strftime('%m'))
        ano = fields.Datetime.now().strftime('%Y')
        return str(dia)+' de '+ str(mes)+' de '+str(ano)

    def get_date_employee(self,fecha):
        fecha_def = ''
        if fecha:
            dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
            mes = self.get_mes(datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m'))
            ano = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
            fecha_def = str(dia)+' de '+ str(mes)+' de '+str(ano)
        return fecha_def

    def get_employee(self,employee_id):
        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)],limit=1)
        return employee      
    
    def get_contract(self,employee_id):
        employee = self.env['hr.contract'].sudo().search([('id', '=', employee_id)],limit=1)
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
            'registro' :  self.env.user.company_id.representante_name or '',
            'rut' :  self.env.user.company_id.representante_rut or '',
            'fechal' : self.env.user.company_id.phone or '',
            'email' : self.env.user.company_id.email or '',
            'comuna' : self.env.user.company_id.comuna or '',

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

    def get_material(self,marital):
        dicmarital = {
            "single":'Soltero(a)',
            "married":'Casado(a)',
            "cohabitant":'Cohabitante Legal',
            "widower":'Viudo(a)',
            "divorced":'Divorciado',
        }
        return dicmarital[str(marital)]