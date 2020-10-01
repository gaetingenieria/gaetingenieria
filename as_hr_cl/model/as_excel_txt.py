from odoo import api, fields, models, _
from odoo.exceptions import UserError

class inventory_excel_extended(models.TransientModel):
    _name= "excel.extended"

    excel_file = fields.Binary(string='Descargar Reporte Excel', readonly=True)
    file_name = fields.Char('Excel File', readonly=True)
    header = fields.Char('Cabecera File', readonly=True)

class inventory_txt_extended(models.TransientModel):
    _name= "txt.extended"

    txt_file = fields.Binary('Descargar formato Previred txt',readonly=True)
    file_name = fields.Char('Txt File', size=64,readonly=True)
