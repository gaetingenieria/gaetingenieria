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
    _name = 'report.as_hr_cl.report_sii_1887.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        #fILTROS
        filtro =''
        if data['form']['as_name_afp']:
            filtro+= ' and hea.id in '+ str(data['form']['as_name_afp']).replace('[','(').replace(']',')')
        if data['form']['employer_id']:
            filtro+= ' and hc.employer_id = '+ str(data['form']['employer_id']).replace('[','(').replace(']',')')
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
        sheet.set_column('K:K',15, letter1)
        sheet.set_column('L:L',15, letter1)

        # Titulos, subtitulos, filtros y campos del reporte
        
        sheet.merge_range('A5:O5', 'PLANILLA SII-1887', titulo1)
        if  data['form']['payslip_run_id']:
            payslip =  self.env[self._context['active_model']].sudo().search([('id', '=', data['form']['payslip_run_id'])])
            filtro +=""" and hp.payslip_run_id="""+str(payslip.id)
        else:
            payslip =  self.env[self._context['active_model']].sudo().search([])
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A1:G1', 'NOMBRE O RAZON SOCIAL:'+str(self.env.user.company_id.name), letter44)
        sheet.merge_range('A2:D2', 'NIT: '+str(self.env.user.company_id.vat), letter444)
        sheet.merge_range('A3:D3', 'Email: '+str(self.env.user.company_id.email)+' Teléfono: '+str(self.env.user.company_id.phone), letter444)
        sheet.merge_range('A4:D4', str(self.env.user.company_id.city)+' '+str(self.env.user.company_id.country_id.name), letter444)
        sheet.merge_range('H1:L1', 'Fecha de impresion: '+fecha, letter444)
        sheet.freeze_panes(7, 0)
        sheet.set_row(7,20,titulo4)

        filas = 7
        
        sheet.write(filas, 0, 'Nro', titulo4)
        sheet.write(filas, 1,'Nombre', titulo4)
        sheet.write(filas, 2,'Empresa', titulo4)
        sheet.write(filas, 3,'Mes remuneracion', titulo4)
        sheet.write(filas, 4,'Imponible', titulo4)
        sheet.write(filas, 5,'Cotizacion trabajador (AFP+fonasa+afc trabajador)', titulo4)
        sheet.write(filas, 6,'Neta', titulo4)
        sheet.write(filas, 7,'No Gravada', titulo4)
        sheet.write(filas, 8,'Impto. Único', titulo4)
        sheet.write(filas, 9,'Factor', titulo4)
        sheet.write(filas, 10,'Imponible + factor', titulo4)
        sheet.write(filas, 11,'Neta + factor', titulo4)
        sheet.write(filas, 12,'NO Gravada + factor', titulo4)
        sheet.write(filas, 13,'Impto. Único + factor', titulo4)
        filas +=1
        cont = 0
        query_movements = ("""
            select hp.id from hr_payslip hp
            join hr_contract hc on hc.id=hp.contract_id
            left join hr_afp hea on hc.afp_id = hea.id
            where 
            hp.state in ('draft','done')
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
        cotizacion = 0.0
        for payslip in payslips:
            cont += 1 
            y=datetime.strptime(str(payslip.date_from), '%Y-%m-%d').strftime('%Y')
            m=datetime.strptime(str(payslip.date_from), '%Y-%m-%d').strftime('%m')
            total_no_gravada = self.get_total_rules(payslip.id,'MOV',payslip.employee_id.id,payslip.contract_id.id)+self.get_total_rules(payslip.id,'COL',payslip.employee_id.id,payslip.contract_id.id)+self.get_total_rules(payslip.id,'VIASAN',payslip.employee_id.id,payslip.contract_id.id)
            cotizacion = float(self.get_total_rules(payslip.id,'PREV',payslip.employee_id.id,payslip.contract_id.id))+float(self.get_total_rules(payslip.id,'SECE',payslip.employee_id.id,payslip.contract_id.id))+float(self.get_total_rules(payslip.id,'SALUD',payslip.employee_id.id,payslip.contract_id.id))+float(self.get_total_rules(payslip.id,'ADISA',payslip.employee_id.id,payslip.contract_id.id))
            imponible= float(self.get_total_rules(payslip.id,'TOTIM',payslip.employee_id.id,payslip.contract_id.id)) * payslip.contract_id.afp_id.sis
            base_tribu= float(self.get_total_rules(payslip.id,'TRIBU',payslip.employee_id.id,payslip.contract_id.id))*payslip.contract_id.afp_id.sis
            no_agravada = total_no_gravada*payslip.contract_id.afp_id.sis


            fecha = str(self.get_mes(m))+'-'+y
            sheet.write(filas, 0, cont, titulo5)
            sheet.write(filas, 1, payslip.employee_id.name, titulo55)
            sheet.write(filas, 2, payslip.contract_id.as_empresa, titulo55)
            sheet.write(filas, 3, fecha, titulo55)
            sheet.write(filas, 4, self.get_total_rules(payslip.id,'TOTIM',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas, 5, cotizacion, number_right)
            sheet.write(filas, 6, self.get_total_rules(payslip.id,'TRIBU',payslip.employee_id.id,payslip.contract_id.id), number_right)
            sheet.write(filas, 7,total_no_gravada, number_right)
            sheet.write(filas, 8,0.0, number_right)
            sheet.write(filas, 9,payslip.contract_id.afp_id.sis, number_right)
            sheet.write(filas, 10,imponible, number_right)
            sheet.write(filas, 11,base_tribu, number_right)
            sheet.write(filas, 12,no_agravada, number_right)
            #totales
            total_13 += self.get_total_rules(payslip.id,'TOTIM',payslip.employee_id.id,payslip.contract_id.id)
            total_14 +=  cotizacion
            total_16 +=  self.get_total_rules(payslip.id,'TRIBU',payslip.employee_id.id,payslip.contract_id.id)
            total_17 += total_no_gravada
            total_18 += imponible
            total_19 += base_tribu
            total_20 += no_agravada
            total_21 += cotizacion
           
            filas +=1
        sheet.merge_range('A'+str(filas+1)+':D'+str(filas+1), 'TOTALES', letter445)  
        sheet.write(filas,4, total_13, number_right_bold) 
        sheet.write(filas,5, total_14, number_right_bold) 
        sheet.write(filas,6, total_16, number_right_bold) 
        sheet.write(filas,7, total_17, number_right_bold) 
        sheet.write(filas,10, total_18, number_right_bold) 
        sheet.write(filas,11, total_19, number_right_bold) 
        sheet.write(filas,12, total_20, number_right_bold) 
     
            
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
            return slip_line.number_of_days
        else:
            return 0.0

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