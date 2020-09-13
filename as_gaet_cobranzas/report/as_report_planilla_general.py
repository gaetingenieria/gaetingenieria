# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime
from odoo import api, models, _
from odoo.exceptions import UserError
from io import BytesIO
from urllib.request import urlopen
from odoo.tools.image import image_data_uri
from odoo.exceptions import UserError
from odoo.exceptions import Warning

class as_kardex_productos_excel(models.AbstractModel):
    _name = 'report.as_gaet_cobranzas.report_planilla_gaet.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):        
        dict_almacen = []
        dict_aux = []
        lotes= []
        filtro = ''
        #restriccion de productos distintos en un mismo reporte
        # product_id =  lines[0].product_id
        # mo_id =  lines[0]
        # generate = True
      
        # if data['form']['stage_id']:
        #     filtro+= ' and hs.id in '+ str(data['form']['stage_id']).replace('[','(').replace(']',')')
        # if data['form']['partner_id']:
        #     filtro+= ' and rp.id in '+ str(data['form']['partner_id']).replace('[','(').replace(']',')')
        # if data['form']['as_empresa']:
        #     filtro+= ' and ae.id in '+ str(data['form']['as_empresa']).replace('[','(').replace(']',')')
        sheet = workbook.add_worksheet('Detalle de Movimientos')
        sheet.set_paper(1)
        sheet.set_landscape()
        
        titulo_color = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True,'bg_color': 'red','border_color':'#000000'})
        titulo_color2 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True,'bg_color': 'yellow','border_color':'#000000'})
        titulo1 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True })
        titulo2 = workbook.add_format({'font_size': 14, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True })
        titulo3_number = workbook.add_format({'font_size': 14, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 11, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True})

        number_left = workbook.add_format({'font_size': 11, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00','bottom': True, 'top': True, 'left': True, 'right': True})
        number_right_colN = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_colB = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00', 'right': True})
        number_right_col1 = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00','font_color':'red'})
        number_right_col1t = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00','font_color':'red','bottom': True, 'top': True, 'left': True, 'right': True})
        number_right = workbook.add_format({'font_size': 11, 'align': 'right', 'num_format': '#,##0.00','bottom': True, 'top': True, 'left': True, 'right': True})
        number_center = workbook.add_format({'font_size': 11, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter12 = workbook.add_format({'font_size': 11, 'align': 'center', 'text_wrap': True, 'bold':True,'bottom': True, 'top': True, 'left': True, 'right': True})
        letter1222 = workbook.add_format({'font_size': 11, 'align': 'center', 'text_wrap': True, 'bold':True})
        letter12B = workbook.add_format({'font_size': 11, 'align': 'center', 'text_wrap': True, 'bold':True,'left': True})
        letter122 = workbook.add_format({'font_size': 11, 'align': 'center', 'text_wrap': True, 'bold':True,'bottom': True, 'top': True, 'left': True, 'right': True,'bg_color': '#FFC0D0',})
        letter11 = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True,'bottom': True, 'top': True, 'left': True, 'right': True,'font_color':'red'})
        letter11L = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True,'bottom': True, 'top': True, 'left': True, 'right': True})
        letter11C = workbook.add_format({'font_size': 11, 'align': 'Center', 'text_wrap': True,'bottom': True, 'top': True, 'left': True, 'right': True})
        letter1 = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True})
        letter1y = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True,'bg_color': 'yellow',})
        letter1C = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True})
        letter1d = workbook.add_format({'font_size': 10, 'align': 'center', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 11, 'align': 'left', 'bold':False})
        letter3 = workbook.add_format({'font_size': 11, 'align': 'right', 'text_wrap': True})
        letter4 = workbook.add_format({'font_size': 11, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter5 = workbook.add_format({'font_size': 11, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter51 = workbook.add_format({'font_size': 11, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',4, letter1)
        sheet.set_column('B:B',15, letter1)
        sheet.set_column('C:C',15, letter1)
        sheet.set_column('D:D',15, letter1)
        sheet.set_column('E:E',15, letter1)
        sheet.set_column('F:F',15, letter1)
        sheet.set_column('G:G',15, letter1)
        sheet.set_column('H:H',15, letter1)
        sheet.set_column('I:I',15, letter1)
        sheet.set_column('J:J',20, letter1)
        sheet.set_column('K:K',15, letter1)
        sheet.set_column('L:L',15, letter1)
        sheet.set_column('M:M',15, letter1)
        url = image_data_uri(self.env.user.company_id.logo)
        image_data = BytesIO(urlopen(url).read())
        sheet.merge_range('B2:J2', self.env.user.company_id.name, titulo_color)
        sheet.insert_image('B3', url, {'image_data': image_data,'x_scale': 0.2, 'y_scale': 0.2})      
        fecha = (datetime.now()- timedelta(hours=5)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('D5:H5', 'Planilla General de Obra', titulo1)
        customer = ''
        if data['form']['as_partner_id']:
            clientes= self.env['res.partner'].search([('id','=', data['form']['as_partner_id'])])
        else:
            clientes= self.env['res.partner'].search([])
        filas = 6
        for cliente in clientes:
            total_sale=0.0
            total=0.0
            total_retenciones=0.0
            total_cancelar=0.0
            invoice = self.env['account.move'].search([('partner_id','=', cliente.id)])
            if invoice:
                sheet.merge_range('A'+str(filas+1)+':M'+str(filas+1), cliente.name, titulo_color2)
                filas += 2
                sheet.merge_range('A'+str(filas+1)+':B'+str(filas+1), '', letter12)
                sheet.write(filas, 2, 'E.E.P.P' ,letter12)   
                sheet.write(filas, 3, 'F. Presentación' ,letter12)   
                sheet.write(filas, 4, 'F. Factura' ,letter12)   
                sheet.write(filas, 5, 'N. Factura' ,letter12)   
                sheet.write(filas, 6, 'Valor Neto' ,letter12)   
                sheet.write(filas, 7, 'Retención' ,letter12)   
                sheet.write(filas, 8, 'Valor Neto a Cancelar' ,letter12)   
                sheet.write(filas, 9, 'I.V.A' ,letter12)   
                sheet.write(filas, 10, 'Total' ,letter12)   
                sheet.write(filas, 11, 'Fecha Pago' ,letter12)   
                sheet.write(filas, 12, 'Estado' ,letter12)   
                filas += 1
                for inv in invoice:
                    sale = self.env['sale.order'].search([('name','=', inv.invoice_origin)])
                    payment = self.env['account.payment'].search([('invoice_ids','=', inv.id)],order='payment_date asc', limit=1)
                    retencion =  ((inv.amount_total*sale.as_retencion.as_porcentaje)/100)
                    total += inv.amount_total
                    total_retenciones+=retencion
                    total_cancelar+=(inv.amount_total-retencion)
                    sheet.merge_range('A'+str(filas+1)+':B'+str(filas+1), cliente.name, letter12)
                    sheet.write(filas, 2, inv.name,letter12) 
                    sheet.write(filas, 3, self.get_fecha_time(sale.as_date_fiscal),letter12) 
                    sheet.write(filas, 4, self.get_fecha(inv.invoice_date),letter12) 
                    sheet.write(filas, 5, inv.as_invoice_number,letter12) 
                    sheet.write(filas, 6, inv.amount_total,number_right_col) 
                    sheet.write(filas, 7, retencion,number_right_col) 
                    sheet.write(filas, 8, (inv.amount_total-retencion),number_right_col) 
                    sheet.write(filas, 9, ((inv.amount_total-retencion)*19)/100,number_right_col) 
                    sheet.write(filas, 10, (inv.amount_total-retencion)+((inv.amount_total-retencion)*19)/100,number_right_col) 
                    sheet.write(filas, 11, self.get_fecha(payment.payment_date),letter12) 
                    sheet.write(filas, 12, self.traduccion(inv.state),letter12) 
                    filas += 1
                filas += 1
                cotizacion = self.env['sale.order'].search([('partner_id','=', cliente.id)])
                for venta in cotizacion:
                    sheet.merge_range('A'+str(filas+1)+':B'+str(filas+1), venta.name, letter12)
                    sheet.write(filas, 2, venta.amount_total,number_right_col) 
                    total_sale +=venta.amount_total
                    filas += 1
                sheet.merge_range('E'+str(filas+1)+':F'+str(filas+1), 'Saldo por Cobrar', letter1y)
                sheet.write(filas, 6, total_sale,number_right_col) 
                filas += 1
                sheet.write(filas, 7,'Retenciones', letter12)
                sheet.write(filas, 8,'Valor Cancelado', letter12)
                filas += 1
                sheet.write(filas, 7, total_retenciones,number_right_col) 
                sheet.write(filas, 8, total_cancelar,number_right_col) 
                filas += 1
            filas += 1

    def get_fecha(self,date):
        fecha =''
        if date:
            fecha = datetime.strptime(str(date), '%Y-%m-%d').strftime('%m/%d/%Y')
        return fecha    
    
    def traduccion(self,data):
        state =''
        if data == 'posted':
            state = 'Publicado'
        elif data == 'draft':
            state = 'Borrador'
        elif data == 'cancel':
            state = 'Cancelado'
        return state

    def get_fecha_time(self,date):
        fecha =''
        if date:
            fecha = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        return fecha