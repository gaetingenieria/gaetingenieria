# -*- coding: utf-8 -*-
from odoo import api, models, fields,_
from odoo.exceptions import UserError
from datetime import datetime
from . import amount_to_text_es
import time
import calendar
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, SU, SA

class ReportTax(models.AbstractModel):
    _name = 'report.as_hr_cl.carta_finiquito'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        employee_id = data['form']['partner_id'][0]
        date = str(data['form']['date'])
        tiempo = data['form']['as_tiempo']
        seguro = data['form']['as_seguro']
        preaviso = data['form']['dias']
        y = data['form']['as_anti_year']
        d = data['form']['as_anti_days']
        m = data['form']['as_anti_mounth']
        mutuo = data['form']['total']
        salario = self.get_salary_total(employee_id,date,tiempo,seguro,mutuo,d,m,y,preaviso,data['form']['contract_id'][0])
        if salario['total'] < 0:
            raise UserError(_("No se puede generar finiquito con un resultado a pagar en negativo."))
        if not self.get_contract(data['form']['contract_id'][0]).date_start:
            raise UserError(_("su contrato no posee fecha inicial."))
        return {
            'data': data['form'],
            'info': self.info_sucursal(),
            'fechas': self.get_date_employee(date),
            'dias': d,
            'total_indem': float(salario['total_indem']),
            'total_previo': float(salario['total_previo']),
            'total_mutuo': salario['total_mutuo'],
            'total_vaca': salario['total_vaca'],
            'total': salario['total'],
            'total_es': amount_to_text_es.amount_to_text(salario['total'],'pesos'),
            'fecha_actual': self.get_date_actual(),
            'employee': self.get_employee(data['form']['partner_id'][0]),
            'contract': self.get_contract(data['form']['contract_id'][0]),
            'articulo': self.get_model_inciso(data['form']['as_articulo_id'][0]),
            'fecha_inicial': self.get_date_employee(self.get_contract(data['form']['contract_id'][0]).date_start),
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
        return str(dia)+' de '+ str(mes)+' de '+str(ano)    
    
    def get_date_actual(self):
        dia = fields.Datetime.now().strftime('%d')
        mes = self.get_mes(fields.Datetime.now().strftime('%m'))
        ano = fields.Datetime.now().strftime('%Y')
        return str(dia)+' de '+ str(mes)+' de '+str(ano)

    def get_employee(self,employee_id):
        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)],limit=1)
        return employee     

    #total de salario 
    def get_salary_total(self,employee_id,date,tiempo,seguro,mutuo,d,m,y,preaviso,contract_id):
        salario_promedio = self.get_employee_salary_prom(employee_id,date,contract_id)
        vacaciones = self.get_employee_amount_vaca(employee_id,d,m,y,date,salario_promedio,contract_id)
        cesantia =0.0
        if preaviso ==False:
            if tiempo > 0:
                cesantia = (salario_promedio*tiempo)-seguro
        mutuo_acuerdo = mutuo
        total = vacaciones+salario_promedio+cesantia+mutuo_acuerdo
        vals={
            'total_indem': round(salario_promedio),
            'total_previo': round(cesantia),
            'total_mutuo': round(mutuo_acuerdo),
            'total_vaca': round(vacaciones),
            'total': round(total),
        }

        return vals

    #calculo de monto de vacaciones
    def get_employee_amount_vaca(self,employee_id,d,m,y,fecha,salario_promedio,contract_id):
        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)],limit=1)
        contract = contract_id
        fac_year = 15
        fac_month = fac_year/12
        fac_days = fac_month /30
        salario_diario = salario_promedio/30
        total_year = y*fac_year
        total_days = d*fac_days
        total_month = m*fac_month
        total_vaca = total_year+total_days+total_month
        total_vaca_price = total_vaca * salario_diario
        total_vaca_price_inh = float(self.get_days_inhabiles(fecha)) * salario_diario
        return total_vaca_price + total_vaca_price_inh

    #calculo de salario promedio
    def get_employee_salary_prom(self,employee_id,date,contract_id):
        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)],limit=1)
        contract = contract_id
        lines_salary=[]  
        mes1= (datetime.strptime(str(date), '%Y-%m-%d') - relativedelta(months=+1)).strftime('%m')
        mes2= (datetime.strptime(str(date), '%Y-%m-%d') - relativedelta(months=+2)).strftime('%m')
        mes3= (datetime.strptime(str(date), '%Y-%m-%d') - relativedelta(months=+3)).strftime('%m')
        year= datetime.strptime(str(date), '%Y-%m-%d').strftime('%Y')
        mes11= str(mes1)+'-'+ self.get_mes(str(mes1))
        mes22= str(mes2)+'-'+ self.get_mes(str(mes2))
        mes33= str(mes3)+'-'+ self.get_mes(str(mes3))
        vals ={
            '1': mes33,
            '2': mes22,
            '3': mes11,
        }
        lines_salary.append(vals)
        vals2={}
        salario_ganado = 0.0
        salario1= self.get_periodo_salary(employee_id,contract_id,str(mes3),year)
        cont=0
        if salario1:
            vals2['1']= salario1
            salario_ganado += salario1
            cont+=1
        else:
            vals2['1']= 0.0
        salario2= self.get_periodo_salary(employee_id,contract_id,str(mes2),year)
        if salario2:
            vals2['2']= salario2
            salario_ganado += salario2
            cont+=1
        else:
            vals2['2']= 0.0
        salario3= self.get_periodo_salary(employee_id,contract_id,str(mes1),year)
        if salario3:
            vals2['3']= salario3
            salario_ganado += salario3
            cont+=1
        else:
            vals2['3']= 0.0
        lines_salary.append(vals2)
        if cont > 0:
            as_salario= salario_ganado/cont
        else:
            as_salario= 0.0
        return as_salario

    def get_periodo_salary(self,employee_id,contract_id,mes,year):
        periodo = calendar.monthrange(int(year),int(mes))
        date_from = str(year)+'-'+str(mes)+'-'+'01'
        date_to = str(year)+'-'+str(mes)+'-'+str(periodo[1])
        self.env.cr.execute("""
            SELECT
                sl.id
            FROM
                hr_payslip sl
            WHERE
                employee_id= """+str(employee_id)+""" and 
                contract_id= """+str(contract_id)+""" and 
                (date_from = '"""+str(date_from)+"""' or
                date_to = '"""+str(date_to)+"""' )
                limit 1
        """)
        ubicaciones_ids = [i[0] for i in self.env.cr.fetchall()]
        monto = 0.0
        if ubicaciones_ids != []:
            slip = self.env['hr.payslip'].search([('id', '=', ubicaciones_ids[0])], limit=1)
            monto += slip._get_salary_line_total('SUELDO')
            monto += slip._get_salary_line_total('BONO')
            monto += slip._get_salary_line_total('COMI')
            monto += slip._get_salary_line_total('COL')
            monto += slip._get_salary_line_total('MOV')
            monto += slip._get_salary_line_total('GRAT')
            monto += slip._get_salary_line_total('HEX50')
        else:
            monto = 0.0
        return monto

    #calculo de dias inhabiles
    def get_days_inhabiles(self,date):
        mes= (datetime.strptime(str(date), '%Y-%m-%d')).strftime('%m')
        year= (datetime.strptime(str(date), '%Y-%m-%d')).strftime('%Y')
        periodo = calendar.monthrange(int(year),int(mes))
        inicio = datetime.strptime(str(periodo[1])+'/'+mes+'/'+year, '%d/%m/%Y')
        fin = datetime.strptime(date, '%Y-%m-%d')
        dt = rrule(freq=DAILY, byweekday=[5,6], dtstart=fin, until=inicio)
        cont =0
        if inicio != fin:
            for day in dt:
                cont+=1
            # dt = pd.bdate_range(start=inicio, end=fin, freq="D")
        return cont

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