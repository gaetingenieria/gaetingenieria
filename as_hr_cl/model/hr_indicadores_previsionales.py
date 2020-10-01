from odoo import api, fields, models, tools, _
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import requests
import requests
import json
import babel

_logger = logging.getLogger(__name__)
MONTH_LIST= [('1', 'Enero'), 
        ('2', 'Febrero'), ('3', 'Marzo'), 
        ('4', 'Abril'), ('5', 'Mayo'), 
        ('6', 'Junio'), ('7', 'Julio'), 
        ('8', 'Agosto'), ('9', 'Septiembre'), 
        ('10', 'Octubre'), ('11', 'Noviembre'),
        ('12', 'Diciembre')]

STATES = {'draft': [('readonly', False)]}

class hr_indicadores_previsionales(models.Model):

    _name = 'hr.indicadores'
    _description = 'Indicadores Previsionales'

    name = fields.Char('Nombre')
    state = fields.Selection([
        ('draft','Borrador'),
        ('done','Validado'),
        ], string=u'Estado', readonly=True, default='draft')
    asignacion_familiar_primer = fields.Float(
        'Asignación Familiar Tramo 1', 
        readonly=True, states=STATES,
        help="Asig Familiar Primer Tramo")
    asignacion_familiar_segundo = fields.Float(
        'Asignación Familiar Tramo 2', 
        readonly=True, states=STATES,
        help="Asig Familiar Segundo Tramo")
    asignacion_familiar_tercer = fields.Float(
        'Asignación Familiar Tramo 3', 
        readonly=True, states=STATES,
        help="Asig Familiar Tercer Tramo")
    asignacion_familiar_monto_a = fields.Float(
        'Monto Tramo Uno', readonly=True, states=STATES, help="Monto A")
    asignacion_familiar_monto_b = fields.Float(
        'Monto Tramo Dos', readonly=True, states=STATES, help="Monto B")
    asignacion_familiar_monto_c = fields.Float(
        'Monto Tramo Tres', readonly=True, states=STATES, help="Monto C")
    contrato_plazo_fijo_empleador = fields.Float(
        'Contrato Plazo Fijo Empleador', 
        readonly=True, states=STATES,
        help="Contrato Plazo Fijo Empleador")
    contrato_plazo_fijo_trabajador = fields.Float(
        'Contrato Plazo Fijo Trabajador', 
        readonly=True, states=STATES,
        help="Contrato Plazo Fijo Trabajador")    
    contrato_plazo_indefinido_empleador = fields.Float(
        'Contrato Plazo Indefinido Empleador', 
        readonly=True, states=STATES,
        help="Contrato Plazo Fijo")
    contrato_plazo_indefinido_empleador_otro = fields.Float(
        'Contrato Plazo Indefinido 11 anos o mas', 
        readonly=True, states=STATES,
        help="Contrato Plazo Indefinido 11 anos Empleador")
    contrato_plazo_indefinido_trabajador_otro = fields.Float(
        'Contrato Plazo Indefinido 11 anos o mas', 
        readonly=True, states=STATES,
        help="Contrato Plazo Indefinido 11 anos Trabajador")
    contrato_plazo_indefinido_trabajador = fields.Float(
        'Contrato Plazo Indefinido Trabajador', 
        readonly=True, states=STATES,
        help="Contrato Plazo Indefinido Trabajador")
    caja_compensacion = fields.Float(
        'Caja Compensación', 
        readonly=True, states=STATES,
        help="Caja de Compensacion")
    deposito_convenido = fields.Float(
        'Deposito Convenido', readonly=True, states=STATES, help="Deposito Convenido")
    fonasa = fields.Float('Fonasa', readonly=True, states=STATES, help="Fonasa")
    mutual_seguridad = fields.Float(
        'Mutualidad', readonly=True, states=STATES, help="Mutual de Seguridad")
    isl = fields.Float(
        'ISL', readonly=True, states=STATES, help="Instituto de Seguridad Laboral")
    pensiones_ips = fields.Float(
        'Pensiones IPS', readonly=True, states=STATES, help="Pensiones IPS")
    sueldo_minimo = fields.Float(
        'Trab. Dependientes e Independientes', readonly=True, states=STATES, help="Sueldo Minimo")    
    sueldo_minimo_prom = fields.Float(
        'Sueldo Minimo Promedio Anual', readonly=True, states=STATES, help="Sueldo Minimo")
    sueldo_minimo_otro = fields.Float(
        'Menores de 18 y Mayores de 65:', 
        readonly=True, states=STATES,
        help="Sueldo Mínimo para Menores de 18 y Mayores a 65")
    tasa_afp_cuprum = fields.Float(
        'Cuprum', readonly=True, states=STATES, help="Tasa AFP Cuprum")
    tasa_afp_capital = fields.Float(
        'Capital', readonly=True, states=STATES, help="Tasa AFP Capital")
    tasa_afp_provida = fields.Float(
        'ProVida', readonly=True, states=STATES, help="Tasa AFP Provida")
    tasa_afp_modelo = fields.Float(
        'Modelo', readonly=True, states=STATES, help="Tasa AFP Modelo")
    tasa_afp_planvital = fields.Float(
        'PlanVital', readonly=True, states=STATES, help="Tasa AFP PlanVital")
    tasa_afp_habitat = fields.Float(
        'Habitat', readonly=True, states=STATES, help="Tasa AFP Habitat")
    tasa_sis_cuprum = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS Cuprum")
    tasa_sis_capital = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS Capital")
    tasa_sis_provida = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS Provida")
    tasa_sis_planvital = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS PlanVital")
    tasa_sis_habitat = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS Habitat")
    tasa_sis_modelo = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa SIS Modelo")
    tasa_independiente_cuprum = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes Cuprum")
    tasa_independiente_capital = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes Capital")
    tasa_independiente_provida = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes Provida")
    tasa_independiente_planvital = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes PlanVital")
    tasa_independiente_habitat = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes Habitat")
    tasa_independiente_modelo = fields.Float(
        'SIS', readonly=True, states=STATES, help="Tasa Independientes Modelo")
    tope_anual_apv = fields.Float(
        'Tope Anual APV', readonly=True, states=STATES, help="Tope Anual APV")
    tope_mensual_apv = fields.Float(
        'Tope Mensual APV', readonly=True, states=STATES, help="Tope Mensual APV")
    tope_imponible_afp = fields.Float(
        'Tope imponible AFP', readonly=True, states=STATES, help="Tope Imponible AFP")
    tope_imponible_ips = fields.Float(
        'Tope Imponible IPS', readonly=True, states=STATES, help="Tope Imponible IPS")
    tope_imponible_salud = fields.Float(
        'Tope Imponible Salud', readonly=True, states=STATES,)
    tope_imponible_seguro_cesantia = fields.Float(
        'Tope Imponible Seguro Cesantía', 
        readonly=True, states=STATES,
        help="Tope Imponible Seguro de Cesantía")
    uf = fields.Float(
        'UF',  required=True, readonly=True, states=STATES, help="UF fin de Mes")
    utm = fields.Float(
        'UTM',  required=True, readonly=True, states=STATES, help="UTM Fin de Mes")    
    as_tope_gratificacion = fields.Float('Tope Gratificación',  help="Tope gratificación")
    uta = fields.Float('UTA', readonly=True, states=STATES, help="UTA Fin de Mes")
    uf_otros = fields.Float(
        'UF Otros', readonly=True, states=STATES, help="UF Seguro Complementario")
    mutualidad_id = fields.Many2one('hr.mutual', 'MUTUAL', readonly=True, states=STATES)
    ccaf_id = fields.Many2one('hr.ccaf', 'CCAF', readonly=True, states=STATES)
    month = fields.Selection(MONTH_LIST, string='Mes', required=True, readonly=True, states=STATES)
    year = fields.Integer('Año', required=True, default=datetime.now().strftime('%Y'), readonly=True, states=STATES)
    gratificacion_legal = fields.Boolean('Gratificación L. Manual', readonly=True, states=STATES)
    mutual_seguridad_bool = fields.Boolean('Mutual Seguridad', default=True, readonly=True, states=STATES)
    ipc = fields.Float(
        'IPC',  required=True, readonly=True, states=STATES, help="Indice de Precios al Consumidor (IPC)")

    def get_previred(self,month_year):
        try:
            urlData = "https://api.gael.cl/general/public/previred/"+month_year
            webURL = urlopen(urlData)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            return json.loads(data.decode(encoding))
        except:
            _logger.debug("/nURL invalid.../n")
            return ""

    def get_salario_promedio(self):
        array_salarys=[]
        total_salarys=[]
        year = (datetime.now()).strftime('%Y')
        month = (datetime.now()).strftime('%m')
        mes = 0
        total_salary = 0
        total_month = 0
        indicadores = self.env['hr.indicadores'].search([('year', '=', year)])
        for indicador in indicadores:
            if not indicador.sueldo_minimo in array_salarys:
                array_salarys.append(indicador.sueldo_minimo)
        for salarys in array_salarys:
            cont = 0
            for indicador in indicadores:
                if indicador.sueldo_minimo == salarys:
                    cont+=1
            vals={'total':salarys*cont,'cont':cont}
            total_salarys.append(vals)
        for mount in total_salarys:
            mes+=int(mount['cont'])
        meses= 12-int(mes)
        salary_actual = self.sueldo_minimo
        total_salarys.append({'total':salary_actual*meses,'cont':meses})
        for mount in total_salarys:
             total_salary+=int(mount['total'])
             total_month+=int(mount['cont'])
        self.sueldo_minimo_prom = total_salary/total_month

    def action_done(self):
        self.write({'state': 'done'})
        return True
    
    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.onchange('month')
    def get_name(self):
        self.name = str(self.month).replace('10', 'Octubre').replace('11', 'Noviembre').replace('12', 'Diciembre').replace('1', 'Enero').replace('2', 'Febrero').replace('3', 'Marzo').replace('4', 'Abril').replace('5', 'Mayo').replace('6', 'Junio').replace('7', 'Julio').replace('8', 'Agosto').replace('9', 'Septiembre') + " " + str(self.year)

    def find_between_r(self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_month(self, s):
        if s == '1':
            return 'Enero'
        if s == '2':
            return 'Febrero'
        if s == '3':
            return 'Marzo'
        if s == '4':
            return 'Abril'
        if s == '5':
            return 'Mayo'
        if s == '6':
            return 'Junio'
        if s == '7':
            return 'Julio'
        if s == '8':
            return 'Agosto'
        if s == '9':
            return 'Septiembre'
        if s == '10':
            return 'Octubre'
        if s == '11':
            return 'Noviembre'
        if s == '12':
            return 'Diciembre'

    def month_year(self):
        month=''
        if self.month == '1':
            month='01'
        elif self.month == '2':
            month='02'
        elif self.month == '3':
            month='03'
        elif self.month == '4':
            month='04'
        elif self.month == '5':
            month='05'
        elif self.month == '6':
            month='06'
        elif self.month == '7':
            month='07'
        elif self.month == '8':
            month='08'
        elif self.month == '9':
            month='09'
        elif self.month == '10':
            month='10'
        elif self.month == '11':
            month='11'
        elif self.month == '12':
            month='12'
        return month+str(self.year)

    def update_document(self):
        try:
            month_year = self.month_year()
            # month_year = self.year + str(self.year)
            obj_json = self.get_previred(month_year)
            
             # UF
            self.uf = float(obj_json['UFValPeriodo'].replace(',','.'))

            # 1 UTM
            self.utm = float(obj_json['UTMVal'].replace(',','.'))

            # 1 UTA
            self.uta = float(obj_json['UTAVal'].replace(',','.'))

            # 3 RENTAS TOPES IMPONIBLES UF
            self.tope_imponible_afp = float(obj_json['RTIAfpUF'].replace(',','.'))
            self.tope_imponible_ips = float(obj_json['RTIIpsUF'].replace(',','.'))
            self.tope_imponible_seguro_cesantia = float(obj_json['RTISegCesUF'].replace(',','.'))

            # 4 RENTAS TOPES IMPONIBLES
            self.sueldo_minimo = float(obj_json['RMITrabDepeInd'].replace(',','.'))
            self.sueldo_minimo_otro = float(obj_json['RMIMen18May65'].replace(',','.'))

            # Ahorro Previsional Voluntario
            self.tope_mensual_apv = float(obj_json['APVTopeMensUF'].replace(',','.'))
            self.tope_anual_apv = float(obj_json['APVTopeAnuUF'].replace(',','.'))

            # 5 DEPÓSITO CONVENIDO
            self.deposito_convenido = float(obj_json['DepConvenidoUF'].replace(',','.'))

            # 6 RENTAS TOPES IMPONIBLES
            self.contrato_plazo_indefinido_empleador = float(obj_json['AFCCpiEmpleador'].replace(',','.'))
            self.contrato_plazo_indefinido_trabajador = float(obj_json['AFCCpiTrabajador'].replace(',','.'))
            self.contrato_plazo_fijo_empleador = float(obj_json['AFCCpfEmpleador'].replace(',','.'))
            self.contrato_plazo_indefinido_empleador_otro = float(obj_json['AFCCpi11Empleador'].replace(',','.'))

            # 7 ASIGNACIÓN FAMILIAR
            self.asignacion_familiar_monto_a = float(obj_json['AFamTramoAMonto'].replace(',','.'))
            self.asignacion_familiar_monto_b = float(obj_json['AFamTramoBMonto'].replace(',','.'))
            self.asignacion_familiar_monto_c = float(obj_json['AFamTramoCMonto'].replace(',','.'))

            self.asignacion_familiar_primer = float(obj_json['AFamTramoAHasta'].replace(',','.'))
            self.asignacion_familiar_segundo = float(obj_json['AFamTramoBHasta'].replace(',','.'))
            self.asignacion_familiar_tercer = float(obj_json['AFamTramoCDesde'].replace(',','.'))

            # 8 TASA COTIZACIÓN OBLIGATORIO AFP
            self.tasa_afp_capital = float(obj_json['AFPCapitalTasaDep'].replace(',','.'))
            self.tasa_sis_capital = float(obj_json['AFPCapitalTasaSIS'].replace(',','.'))

            self.tasa_afp_cuprum = float(obj_json['AFPCuprumTasaDep'].replace(',','.'))
            self.tasa_sis_cuprum = float(obj_json['AFPCuprumTasaSIS'].replace(',','.'))

            self.tasa_afp_habitat = float(obj_json['AFPHabitatTasaDep'].replace(',','.'))
            self.tasa_sis_habitat = float(obj_json['AFPHabitatTasaSIS'].replace(',','.'))

            self.tasa_afp_planvital = float(obj_json['AFPPlanVitalTasaDep'].replace(',','.'))
            self.tasa_sis_planvital = float(obj_json['AFPPlanVitalTasaSIS'].replace(',','.'))

            self.tasa_afp_provida = float(obj_json['AFPProVidaTasaDep'].replace(',','.'))
            self.tasa_sis_provida = float(obj_json['AFPProVidaTasaSIS'].replace(',','.'))

            self.tasa_afp_modelo = float(obj_json['AFPModeloTasaDep'].replace(',','.'))
            self.tasa_sis_modelo = float(obj_json['AFPModeloTasaSIS'].replace(',','.'))

            self.tasa_independiente_capital = float(obj_json['AFPCapitalTasaInd'].replace(',','.'))
            self.tasa_independiente_cuprum = float(obj_json['AFPCuprumTasaInd'].replace(',','.'))
            self.tasa_independiente_habitat = float(obj_json['AFPHabitatTasaInd'].replace(',','.'))
            self.tasa_independiente_planvital = float(obj_json['AFPPlanVitalTasaInd'].replace(',','.'))
            self.tasa_independiente_provida = float(obj_json['AFPProVidaTasaInd'].replace(',','.'))
            self.tasa_independiente_modelo = float(obj_json['AFPModeloTasaInd'].replace(',','.'))
            self.get_salario_promedio()

        except ValueError:
            return ""
