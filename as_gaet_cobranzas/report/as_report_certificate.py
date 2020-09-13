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
    _name = 'report.as_gaet_cobranzas.report_cobranza_gaet.xlsx'
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
        titulo_color2 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True,'bg_color': '#FFC0D0','border_color':'#000000'})
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
        url = image_data_uri(self.env.user.company_id.logo)
        image_data = BytesIO(urlopen(url).read())
        sheet.merge_range('B2:J2', self.env.user.company_id.name, titulo_color)
        sheet.insert_image('B3', url, {'image_data': image_data,'x_scale': 0.2, 'y_scale': 0.2})      
        fecha = (datetime.now()- timedelta(hours=5)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('D5:H5', 'Resumen Global de la Obra', titulo_color2)
        sheet.insert_image('I3', url, {'image_data': image_data,'x_scale': 0.2, 'y_scale': 0.2}) 
        customer = ''
        #1
        sheet.write(7, 1, 'Presupuesto: ',letter12) 
        sheet.write(7, 2, lines.name ,letter11)   
        sheet.write(7, 3, 'Valor Contrato: ',letter12) 
        sheet.write(7, 4, lines.amount_untaxed ,letter11) 
        sheet.write(7, 7, 'Medio de Pago: ',letter12) 
        sheet.write(7, 8, lines.as_medio_pago.name ,letter11) 
        #2
        sheet.write(9, 1, 'Obra: ',letter12) 
        sheet.write(9, 2, lines.client_order_ref,letter11)   
        sheet.write(9, 3, 'IVA 19%: ',letter12) 
        sheet.write(9, 4, lines.amount_tax ,letter11) 
        sheet.write(9, 7, 'Tipo de Garantía: ',letter12) 
        sheet.write(9, 8, lines.as_tipo_garantia ,letter11) 
        #3
        sheet.write(11, 1, 'Mandante: ',letter12) 
        sheet.write(11, 2, lines.partner_id.name,letter11)   
        sheet.write(11, 3, 'Total + IVA: ',letter12) 
        sheet.write(11, 4, lines.amount_total ,letter11) 
        sheet.write(11, 7, 'Fecha Vencimiento: ',letter12) 
        sheet.write(11, 8, lines.validity_date ,letter11)         
        #4
        sheet.write(13, 1, 'Dirección: ',letter12) 
        sheet.merge_range('C14:E14', lines.partner_id.street, letter11)
        sheet.write(13, 7, 'Retención: ',letter12) 
        sheet.write(13, 8, str(lines.as_retencion.as_porcentaje)+'%' ,letter11)  
        #4
        sheet.write(15, 1, 'Resp. Obra: ',letter12) 
        sheet.write(15, 2, lines.user_id.partner_id.name,letter11)   
        sheet.write(15, 3, 'Tope Retención: ',letter12) 
        sheet.write(15, 4, lines.as_retencion.as_tope ,letter11) 
        sheet.merge_range('D18:H18', 'Resumen EEPP de la Obra', titulo_color2)
        sheet.write(19, 1, 'N°',letter122)
        sheet.write(19, 2, 'Presentación',letter122)
        sheet.write(19, 3, 'Valor EEPP',letter122)
        sheet.write(19, 4, 'Retención',letter122)
        sheet.write(19, 5, 'Valor Neto',letter122)
        sheet.write(19, 6, 'Iva 19%',letter122)
        sheet.write(19, 7, 'Total',letter122)
        sheet.write(19, 8, 'Por cobrar',letter122)
        sheet.write(19, 9, 'Avance',letter122)
        filas = 20
        total_eepp = 0.0
        total_retencion = 0.0
        total_valor_neto = 0.0
        total_iva = 0.0
        total_total = 0.0
        for inv in lines.invoice_ids:
            retencion = (inv.amount_total*lines.as_retencion.as_porcentaje)/100
            sheet.write(filas, 1, inv.name,letter12B)
            sheet.write(filas, 2, self.get_fecha(inv.invoice_date),letter1222)
            sheet.write(filas, 3, inv.amount_total,number_right_col1)
            sheet.write(filas, 4, retencion,number_right_col1)
            sheet.write(filas, 5, inv.amount_total-retencion,number_right_col1)
            sheet.write(filas, 6, inv.amount_tax,number_right_col1)
            sheet.write(filas, 7, (inv.amount_total-retencion)+inv.amount_tax,number_right_col1)
            sheet.write(filas, 8, inv.amount_total,number_right_colN)
            sheet.write(filas, 9, lines.amount_untaxed/inv.amount_total,number_right_colB)
            total_eepp += inv.amount_total
            total_retencion += retencion
            total_valor_neto += inv.amount_total-retencion
            total_iva += inv.amount_tax
            total_total += (inv.amount_total-retencion)+inv.amount_tax
            filas += 1
        sheet.merge_range('B'+str(filas+1)+':C'+str(filas+1), 'Totales', letter12)
        sheet.write(filas, 3, total_eepp,number_right_col1t)
        sheet.write(filas, 4, total_retencion,number_right_col1t)
        sheet.write(filas, 5, total_valor_neto,number_right_col1t)
        sheet.write(filas, 6, total_iva,number_right_col1t)
        sheet.write(filas, 7, total_total,number_right_col1t)
        sheet.write(filas, 8, '',number_right_col1t)
        sheet.write(filas, 9, '',number_right_col1t)
        filas += 2
        sheet.merge_range('D'+str(filas+1)+':H'+str(filas+1), 'Presupuesto de Obra', titulo_color2)
        filas += 2
        sheet.write(filas, 1, 'N° Item',letter122)
        sheet.merge_range('C'+str(filas+1)+':F'+str(filas+1), 'Totales', letter122)
        sheet.write(filas, 6, 'Cantidad ',letter122)
        sheet.write(filas, 7, 'Unidad ',letter122)
        sheet.write(filas, 8, 'Valor Unitario ',letter122)
        sheet.write(filas, 9, 'Total ',letter122)
        filas += 1
        cont = 0
        for line in lines.order_line:
            cont+=1
            sheet.write(filas, 1, cont,letter11C)
            sheet.merge_range('C'+str(filas+1)+':F'+str(filas+1), line.product_id.name, letter11L)
            sheet.write(filas, 6, line.product_uom_qty,letter11C)
            sheet.write(filas, 7, line.product_uom.name,letter11C)
            sheet.write(filas, 8, line.price_unit,number_right)
            sheet.write(filas, 9, line.product_uom_qty*line.price_unit,number_right)
            filas += 1





    def get_fecha(self,date):
        fecha =''
        if date:
            fecha = datetime.strptime(str(date), '%Y-%m-%d').strftime('%m/%d/%Y')
        return fecha