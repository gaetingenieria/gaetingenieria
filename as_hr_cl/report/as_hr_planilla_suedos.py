# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime
import logging
_logger = logging.getLogger(__name__)

class as_sales_emit_excel(models.AbstractModel):
    _name = 'report.as_hr_cl.planilla_sueldos.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        #fILTROS
        filtro =''
        if data['form']['as_name_afp']:
            filtro+= ' and hea.id in '+ str(data['form']['as_name_afp']).replace('[','(').replace(']',')')
            
        #estilos
        sheet = workbook.add_worksheet('Resumen de ventas')
        titulo1 = workbook.add_format({'font_size': 13, 'align': 'center', 'text_wrap': True, 'bold':True })
        titulo2 = workbook.add_format({'font_size': 8, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 8, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3_number = workbook.add_format({'font_size': 8, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 8, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })
        titulo10 = workbook.add_format({'font_size': 8, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })
        titulo5 = workbook.add_format({'font_size': 8, 'align': 'center', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False })
        titulo55 = workbook.add_format({'font_size': 8, 'align': 'left', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False })
        titulo9 = workbook.add_format({'font_size': 8, 'align': 'right', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False })
        titulo6 = workbook.add_format({'font_size': 8, 'align': 'center', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False, 'color': 'red'})
        titulo12 = workbook.add_format({'font_size': 8, 'align': 'right', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False, 'color': 'red'})
        titulo7 = workbook.add_format({'font_size': 8, 'align': 'left', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False})
        titulo8 = workbook.add_format({'font_size': 8, 'align': 'center', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':True})

        number_left = workbook.add_format({'font_size': 8, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 8, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 8, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 8, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_center = workbook.add_format({'font_size': 8, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter1 = workbook.add_format({'font_size': 8, 'align': 'left', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 8, 'align': 'left', 'bold':True})
        letter3 = workbook.add_format({'font_size': 8, 'align': 'right', 'text_wrap': True})
        letter4 = workbook.add_format({'font_size': 8, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter444 = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter44 = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter445 = workbook.add_format({'font_size': 9, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter_locked = letter3
        letter_locked.set_locked(False)

        filtro_afp = data['form']['as_name_afp']
        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',7, letter1)
        sheet.set_column('B:B',25, letter1)
        sheet.set_column('C:C',12, letter1)
        sheet.set_column('D:D',10, letter1)
        sheet.set_column('E:E',10, letter1)
        sheet.set_column('F:F',8, letter1)
        sheet.set_column('G:G',15, letter1)
        sheet.set_column('H:H',9, letter1)
        sheet.set_column('I:I',9, letter1)
        sheet.set_column('J:J',7, letter1)
        sheet.set_column('K:K',7, letter1)

        # Titulos, subtitulos, filtros y campos del reporte
        sheet.merge_range('A5:O5', 'LIBRO DE REMUNERACIONES', titulo1)
        payslip =  self.env[self._context['active_model']].sudo().search([('id', '=', data['form']['payslip_run_id'])])
        fecha_inicial = datetime.strptime(str(payslip.date_start), '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(str(payslip.date_end), '%Y-%m-%d').strftime('%d/%m/%Y')
        sheet.merge_range('A6:O6', 'PERIODO: '+fecha_inicial +' - '+ fecha_final, titulo1)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A1:G1', 'NOMBRE O RAZON SOCIAL:'+str(self.env.user.company_id.name), letter44)
        sheet.merge_range('A2:D2', 'NIT: '+str(self.env.user.company_id.vat), letter444)
        sheet.merge_range('A3:D3', 'Email: '+str(self.env.user.company_id.email)+' Teléfono: '+str(self.env.user.company_id.phone), letter444)
        sheet.merge_range('A4:D4', str(self.env.user.company_id.city)+' '+str(self.env.user.company_id.country_id.name), letter444)
        sheet.merge_range('H1:L1', 'Fecha de impresion: '+str(fecha), letter444)
        sheet.freeze_panes(7, 0)
        sheet.set_row(7,20,titulo4)

        filas = 7
        sheet.write(filas, 0, 'Nro', titulo4)
        sheet.write(filas, 1, 'Nombre Trabajador', titulo4)
        sheet.write(filas, 2, 'RUT', titulo4)
        sheet.write(filas, 3, 'Contrato', titulo4)
        sheet.write(filas, 4, 'UF', titulo4)
        sheet.write(filas, 5, 'UTM ', titulo4)
        sheet.write(filas, 6, 'Periodo', titulo4)
        sheet.write(filas, 7, 'Desde', titulo4)
        sheet.write(filas, 8, 'Hasta', titulo4)
        sheet.write(filas, 9, 'Dias Totales', titulo4)
        sheet.write(filas, 10, 'Dias Ausentes', titulo4)
        sheet.write(filas, 11, 'Dias Trabajados', titulo4)
        sheet.write(filas, 12, 'Sueldo Base', titulo4)
        sheet.write(filas, 13, 'Sueldo Base', titulo4)
        sheet.write(filas, 14, 'Gratificacion', titulo4)
        sheet.write(filas, 15, 'Cant HH', titulo4)
        sheet.write(filas, 16, 'Valor HH', titulo4)
        sheet.write(filas, 17, 'Comisiones', titulo4)
        sheet.write(filas, 18, 'Vacaciones', titulo4)
        sheet.write(filas, 19, 'Total Imponible', titulo4)
        sheet.write(filas, 20, 'Familiar', titulo4)
        sheet.write(filas, 21, 'Viaticos', titulo4)
        sheet.write(filas, 22, 'Movilizacion', titulo4)
        sheet.write(filas, 23, 'Colacion', titulo4)
        sheet.write(filas, 24, 'Total Haberes', titulo4)
        sheet.write(filas, 25, 'Nombre AFP', titulo4)
        sheet.write(filas, 26, 'Tasa AFP', titulo4)
        sheet.write(filas, 27, 'Total AFP', titulo4)
        sheet.write(filas, 28, 'Entidad Salud', titulo4)
        sheet.write(filas, 29, 'Plan Isapre UF', titulo4)
        sheet.write(filas, 30, '7%', titulo4)
        sheet.write(filas, 31, 'Adicional Salud', titulo4)
        sheet.write(filas, 32, 'Caja Comp', titulo4)
        sheet.write(filas, 33, 'AFC', titulo4)
        sheet.write(filas, 34, 'Base Tributario', titulo4)
        sheet.write(filas, 35, 'Impuesto ', titulo4)
        sheet.write(filas, 36, 'Total Desc', titulo4)
        sheet.write(filas, 37, 'Total a Pago ', titulo4)
        sheet.write(filas, 38, 'Anticipo ', titulo4)
        sheet.write(filas, 39, 'A Liquidar ', titulo4)
        filas +=1
        cont = 0
        query_movements = ("""
            select hp.id from hr_payslip hp
            join hr_contract hc on hc.id=hp.contract_id
            left join hr_afp hea on hc.afp_id = hea.id
            where 
            hp.state in ('draft','done')
            and hp.payslip_run_id="""+str(payslip.id)+"""
            """+filtro+"""
            """)
        #_logger.debug(query_movements)
        self.env.cr.execute(query_movements)
        slip = [k for k in self.env.cr.fetchall()] 
        payslips = self.env['hr.payslip'].sudo().search([('id', 'in', slip)])
        total_desc= 0.0
        total_liq= 0.0
        total_13=0.0
        total_14=0.0
        total_16=0.0
        total_17=0.0
        total_18=0.0
        total_19=0.0
        total_20=0.0
        total_21=0.0
        total_22=0.0
        total_23=0.0
        total_24=0.0
        total_27=0.0
        total_30=0.0
        total_31=0.0
        total_32=0.0
        total_33=0.0
        total_34=0.0
        total_35=0.0
        total_36=0.0
        total_37=0.0
        total_38=0.0
        total_39=0.0
        for payslip in payslips:
            cont += 1 
            sheet.write(filas, 0, cont, titulo5)
            sheet.write(filas, 1, payslip.employee_id.name, titulo55)
            sheet.write(filas, 2, payslip.employee_id.identification_id, titulo55)
            sheet.write(filas, 3, payslip.contract_id.name, titulo55)
            sheet.write(filas, 4, payslip.indicadores_id.uf, number_right)
            sheet.write(filas, 5, payslip.indicadores_id.utm, number_right)
            sheet.write(filas, 6, str(payslip.indicadores_id.month)+'-'+str(payslip.indicadores_id.year), titulo55)
            sheet.write(filas, 7, datetime.strptime(str(payslip.date_from), '%Y-%m-%d').strftime('%d/%m/%Y'), titulo55)
            sheet.write(filas, 8, datetime.strptime(str(payslip.date_to), '%Y-%m-%d').strftime('%d/%m/%Y'), titulo55)
            sheet.write(filas, 9, str(payslip.contract_id.resource_calendar_id.as_total_days), number_right)
            sheet.write(filas, 10, str(self.get_total_working(payslip.id,2)), number_right)
            sheet.write(filas, 11, str(self.get_total_working(payslip.id,1)), number_right)
            sheet.write(filas, 12, payslip.contract_id.wage, number_right)
            sheet.write(filas,13, self.get_total_rules(payslip.id,'SUELDO',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,14, self.get_total_rules(payslip.id,'GRAT',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,15, str(self.get_total_input(payslip.id,'HEX50')), number_right)
            sheet.write(filas,16, self.get_total_rules(payslip.id,'HEX50',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,17, self.get_total_rules(payslip.id,'COMI',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,18, self.get_total_rules(payslip.id,'VACA',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,19, self.get_total_rules(payslip.id,'TOTIM',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,20, self.get_total_rules(payslip.id,'ASIGFAM',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,21, self.get_total_rules(payslip.id,'VIASAN',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,22, self.get_total_rules(payslip.id,'MOV',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,23, self.get_total_rules(payslip.id,'COL',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,24, self.get_total_rules(payslip.id,'HAB',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,25, payslip.contract_id.afp_id.name, titulo55)
            sheet.write(filas,26, payslip.contract_id.afp_id.rate, number_right)
            sheet.write(filas,27, self.get_total_rules(payslip.id,'SIS',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,28, payslip.contract_id.isapre_id.name, titulo55)
            sheet.write(filas,29, payslip.contract_id.isapre_cotizacion_uf, number_right)
            sheet.write(filas,30, self.get_total_rules(payslip.id,'SALUD',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,31, self.get_total_rules(payslip.id,'ADISA',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,32, self.get_total_rules(payslip.id,'CAJACOMP',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,33, self.get_total_rules(payslip.id,'SECE',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,34, self.get_total_rules(payslip.id,'TRIBU',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,35, self.get_total_rules(payslip.id,'IMPUNI',payslip.employee_id.id,payslip.contract_id.id), number_right)
            total_desc +=self.get_total_rules(payslip.id,'IMPUNI',payslip.employee_id.id,payslip.contract_id.id)
            total_liq +=self.get_total_rules(payslip.id,'LIQ',payslip.employee_id.id,payslip.contract_id.id)
            sheet.write(filas,36, self.get_total_rules(payslip.id,'TOD',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,37, float(self.get_total_rules(payslip.id,'LIQ',payslip.employee_id.id,payslip.contract_id.id))+float(self.get_total_rules(payslip.id,'ASUE',payslip.employee_id.id,payslip.contract_id.id)), number_right)
            sheet.write(filas,38, self.get_total_rules(payslip.id,'ASUE',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas,39, float(self.get_total_rules(payslip.id,'LIQ',payslip.employee_id.id,payslip.contract_id.id))-float(self.get_total_rules(payslip.id,'ASUE',payslip.employee_id.id,payslip.contract_id.id)), number_right)
            #totales
            total_13 += self.get_total_rules(payslip.id,'SUELDO',payslip.employee_id.id,payslip.contract_id.id)
            total_14 += self.get_total_rules(payslip.id,'GRAT',payslip.employee_id.id,payslip.contract_id.id)
            total_16 += self.get_total_rules(payslip.id,'HEX50',payslip.employee_id.id,payslip.contract_id.id)
            total_17 += self.get_total_rules(payslip.id,'COMI',payslip.employee_id.id,payslip.contract_id.id)
            total_18 += self.get_total_rules(payslip.id,'VACA',payslip.employee_id.id,payslip.contract_id.id)
            total_19 += self.get_total_rules(payslip.id,'TOTIM',payslip.employee_id.id,payslip.contract_id.id)
            total_20 += self.get_total_rules(payslip.id,'ASIGFAM',payslip.employee_id.id,payslip.contract_id.id)
            total_21 += self.get_total_rules(payslip.id,'VIASAN',payslip.employee_id.id,payslip.contract_id.id)
            total_22 += self.get_total_rules(payslip.id,'MOV',payslip.employee_id.id,payslip.contract_id.id)
            total_23 += self.get_total_rules(payslip.id,'COL',payslip.employee_id.id,payslip.contract_id.id)
            total_24 += self.get_total_rules(payslip.id,'HAB',payslip.employee_id.id,payslip.contract_id.id)
            total_27 += self.get_total_rules(payslip.id,'SIS',payslip.employee_id.id,payslip.contract_id.id)
            total_30 += self.get_total_rules(payslip.id,'SALUD',payslip.employee_id.id,payslip.contract_id.id)
            total_31 += self.get_total_rules(payslip.id,'ADISA',payslip.employee_id.id,payslip.contract_id.id)
            total_32 += self.get_total_rules(payslip.id,'CAJACOMP',payslip.employee_id.id,payslip.contract_id.id)
            total_33 += self.get_total_rules(payslip.id,'SECE',payslip.employee_id.id,payslip.contract_id.id)
            total_34 += self.get_total_rules(payslip.id,'TRIBU',payslip.employee_id.id,payslip.contract_id.id)
            total_35 += self.get_total_rules(payslip.id,'IMPUNI',payslip.employee_id.id,payslip.contract_id.id)
            total_36 += self.get_total_rules(payslip.id,'TOD',payslip.employee_id.id,payslip.contract_id.id)
            total_37 += float(self.get_total_rules(payslip.id,'LIQ',payslip.employee_id.id,payslip.contract_id.id))
            total_38 += self.get_total_rules(payslip.id,'ASUE',payslip.employee_id.id,payslip.contract_id.id)
            total_39 += float(self.get_total_rules(payslip.id,'LIQ',payslip.employee_id.id,payslip.contract_id.id))
            filas +=1
        sheet.merge_range('A'+str(filas+1)+':L'+str(filas+1), 'TOTALES', letter445)  
        sheet.write(filas,13, total_13, number_right_bold) 
        sheet.write(filas,14, total_14, number_right_bold) 
        sheet.write(filas,16, total_16, number_right_bold) 
        sheet.write(filas,17, total_17, number_right_bold) 
        sheet.write(filas,18, total_18, number_right_bold) 
        sheet.write(filas,19, total_19, number_right_bold) 
        sheet.write(filas,20, total_20, number_right_bold) 
        sheet.write(filas,21, total_21, number_right_bold) 
        sheet.write(filas,22, total_22, number_right_bold) 
        sheet.write(filas,23, total_23, number_right_bold) 
        sheet.write(filas,24, total_24, number_right_bold) 
        sheet.write(filas,27, total_27, number_right_bold) 
        sheet.write(filas,30, total_30, number_right_bold) 
        sheet.write(filas,31, total_31, number_right_bold) 
        sheet.write(filas,32, total_32, number_right_bold) 
        sheet.write(filas,33, total_33, number_right_bold) 
        sheet.write(filas,34, total_34, number_right_bold) 
        sheet.write(filas,35, total_35, number_right_bold) 
        sheet.write(filas,36, total_36, number_right_bold) 
        sheet.write(filas,37, total_37, number_right_bold) 
        sheet.write(filas,38, total_38, number_right_bold) 
        sheet.write(filas,39, total_39, number_right_bold) 
     
    def get_total_rules(self,slip_id,code,employee_id,contract_id): 
        slip_line=self.env['hr.payslip.line'].sudo().search([('slip_id', '=', slip_id),('code', '=',code),('contract_id', '=',contract_id)],limit=1)
        if slip_line:
            return slip_line.total
        else:
            return 0.0    
    
    def get_total_working(self,slip_id,id): 
        slip_line=self.env['hr.payslip.worked_days'].sudo().search([('payslip_id', '=', slip_id),('work_entry_type_id', '=',id)],limit=1)
        if slip_line:
            return slip_line.number_of_days
        else:
            return 0.0    

    def get_total_input(self,slip_id,code): 

        type_input=self.env['hr.payslip.input.type'].sudo().search([('code', '=',code)],limit=1)
        slip_line=self.env['hr.payslip.input'].sudo().search([('payslip_id', '=', slip_id),('input_type_id', '=',type_input.id)],limit=1)
        if slip_line:
            return slip_line.amount
        else:
            return 0.0

