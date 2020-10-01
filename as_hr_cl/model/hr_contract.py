from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from . import amount_to_text_es
from datetime import datetime
from dateutil.relativedelta import relativedelta

class hr_contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    afp_id = fields.Many2one('hr.afp', 'AFP')
    anticipo_sueldo = fields.Float('Anticipo de Sueldo',help="Anticipo De Sueldo Realizado Contablemente")
    carga_familiar = fields.Integer('Carga Simple',help="Carga familiar para el cálculo de asignación familiar simple")
    carga_familiar_maternal = fields.Integer('Carga Maternal',help="Carga familiar para el cálculo de asignación familiar maternal")
    carga_familiar_invalida = fields.Integer('Carga Inválida',help="Carga familiar para el cálculo de asignación familiar inválida")            
    colacion = fields.Float('Asig. Colación', help="Colación")
    isapre_id = fields.Many2one('hr.isapre', 'Nombre')
    isapre_cotizacion_uf = fields.Float('Cotización', digits=(6, 4),  help="Cotización Pactada")  
    isapre_fun = fields.Char('Número de FUN',  help="Indicar N° Contrato de Salud a Isapre") 
    isapre_cuenta_propia = fields.Boolean('Isapre Cuenta Propia')   
    movilizacion = fields.Float('Asig. Movilización', help="Movilización")
    mutual_seguridad = fields.Boolean('Mutual Seguridad', default=True)
    otro_no_imp = fields.Float('Otros No Imponible', help="Otros Haberes No Imponibles")
    otros_imp = fields.Float('Otros Imponible', help="Otros Haberes Imponibles")
    pension = fields.Boolean('Pensionado')
    sin_afp = fields.Boolean('No Calcula AFP')
    sin_afp_sis = fields.Boolean('No Calcula AFP SIS')
    seguro_complementario_id = fields.Many2one('hr.seguro.complementario', 'Nombre')
    seguro_complementario = fields.Float('Cotización',  help="Seguro Complementario")
    viatico_santiago = fields.Float('Asig. Viático',  help="Asignación de Viático")
    complete_name = fields.Char(related='employee_id.firstname')
    last_name = fields.Char(related='employee_id.last_name')
    gratificacion_legal = fields.Boolean('Gratificación L. Manual')
    as_gratificacion_legal = fields.Float('Gratificación L. (%))',default=25)
    isapre_moneda= fields.Selection([('uf', 'UF'), ('clp', 'Pesos')], 'Tipo de Moneda', default="uf")
    apv_id = fields.Many2one('hr.apv', 'Nombre')
    aporte_voluntario = fields.Float('Ahorro Previsional Voluntario (APV)', help="Ahorro Previsional Voluntario (APV)")
    aporte_voluntario_moneda= fields.Selection([('uf', 'UF'), ('clp', 'Pesos')], 'Tipo de Moneda', default="uf")
    forma_pago_apv = fields.Selection([('1', 'Directa'), ('2', 'Indirecta')], 'Forma de Pago', default="1")
    seguro_complementario_moneda= fields.Selection([('uf', 'UF'), ('clp', 'Pesos')], 'Tipo de Moneda', default="uf")
    as_empresa= fields.Selection([('Class', 'Class'), ('Fund', 'Fund'), ('Group', 'Group')], 'Tipo de empresa', default="Class")
    file_contract = fields.Binary('Contrato')

    def get_amount(self,amount):
        return amount_to_text_es.amount_to_text(amount,self.currency_id)

    def get_date_literal(self,fecha):
        dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
        mes = self.get_mes(datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m'))
        ano = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
        return str(dia)+' de '+ str(mes)+' de '+str(ano)

    @api.onchange('employee_id')
    def get_name_employee(self):
        if self.employee_id:
            self.name= self.employee_id.name

    def get_printer_report(self):
        self.ensure_one()
        context = self._context
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        # pdf = self.env.ref('as_hr_cl.as_hr_cl_anexo_contrato_report')
        # modelo = 'hr.employee'
        # content, content_type = self.env.ref('as_hr_cl.as_hr_cl_anexo_contrato_report').render_qweb_pdf(self, data=data)
        # self.env['ir.attachment'].create({
        #     'name': self.partner_id.name and _("Aexos de Contrato %s.pdf") % self.partner_id.name or _("Aexos de Contrato.pdf"),
        #     'type': 'binary',
        #     'datas': base64.encodestring(content),
        #     'res_model': modelo,
        #     'res_id': self.partner_id.id,
        # })
        return self.env.ref('as_hr_cl.as_hr_cl_anexo_contrato_report').report_action(self, data=data)


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

    def info_sucursal(self):
        info = ''
        contract = self.employer_id
        diccionario_dosificacion= {}
        diccionario_dosificacion = {
            'nombre_empresa' : contract.name or '',
            'nit' : contract.rut or '',
            'direccion1' : contract.address or '',
            'telefono' : self.env.user.company_id.phone or '',
            'ciudad' : self.env.user.company_id.city or '',
            'sucursal' : self.env.user.company_id.city or '',
            'pais' : self.env.user.company_id.country_id.name or '',
            'actividad' :  self.env.user.company_id.name or '',
            'registro' :  contract.representante_name or '',
            'rut' :  contract.representante_rut or '',
            'fechal' : self.env.user.company_id.phone or '',
            'email' : self.env.user.company_id.email or '',
            'comuna' : contract.comuna or '',

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

    def get_days(self,days):
        daysesDic = {
            "0":'Lunes',
            "1":'Martes',
            "2":'Miercoles',
            "3":'Jueves',
            "4":'Viernes',
            "5":'Sabado',
            "6":'Domingo',
        }
        return daysesDic[str(days)]

    def get_material(self,marital):
        dicmarital = {
            "single":'Soltero(a)',
            "married":'Casado(a)',
            "cohabitant":'Cohabitante Legal',
            "widower":'Viudo(a)',
            "divorced":'Divorciado',
        }
        return dicmarital[str(marital)]

    def get_horario(self):
        horario = []
        tarde = []
        for hours in self.resource_calendar_id.attendance_ids:
            if hours.day_period == 'morning':
                if horario ==[]:
                    vals = {
                        'turn':hours.day_period,
                        'day':self.get_days(str(hours.dayofweek)),
                        'hour_from':hours.hour_from,
                        'hour_to':hours.hour_to,
                    }
                    horario.append(vals)
                else:
                    for array_days in horario:
                        if array_days['hour_from'] == hours.hour_from and array_days['hour_to']==hours.hour_to:
                            array_days['day']+= ','+self.get_days(str(hours.dayofweek))
                        else:
                            vals = {
                                'turn':hours.day_period,
                                'day':self.get_days(str(hours.dayofweek)),
                                'hour_from':hours.hour_from,
                                'hour_to':hours.hour_to,
                            }
                            horario.append(vals)
        for hours in self.resource_calendar_id.attendance_ids:
            if hours.day_period != 'morning':
                if tarde ==[]:
                    vals = {
                        'turn':hours.day_period,
                        'day':self.get_days(str(hours.dayofweek)),
                        'hour_from':hours.hour_from,
                        'hour_to':hours.hour_to,
                    }
                    tarde.append(vals)
                else:
                    for array_days in tarde:
                        if array_days['hour_from'] == hours.hour_from and array_days['hour_to']==hours.hour_to:
                            array_days['day']+= ','+self.get_days(str(hours.dayofweek))
                        else:
                            vals = {
                                'turn':hours.day_period,
                                'day':self.get_days(str(hours.dayofweek)),
                                'hour_from':hours.hour_from,
                                'hour_to':hours.hour_to,
                            }
                            tarde.append(vals)
        return horario+tarde
                    





