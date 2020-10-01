from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from . import amount_to_text_es
from datetime import datetime
from dateutil.relativedelta import relativedelta

class hr_contract(models.Model):
    _inherit = 'as.hr.employer'
    _description = 'herencia del modelo empleador'


    mutual_seguridad = fields.Float(
        'Mutualidad',help="Mutual de Seguridad")
    isl = fields.Float(
        'ISL',help="Instituto de Seguridad Laboral")
    ccaf_id = fields.Many2one('hr.ccaf', 'CCAF')
    mutual_seguridad_bool = fields.Boolean('Mutual Seguridad', default=True)
    mutualidad_id = fields.Many2one('hr.mutual', 'MUTUAL')
    caja_compensacion = fields.Float('Caja Compensación', help="Caja de Compensacion")
    fonasa = fields.Float('Fonasa', help="Fonasa")
    tope_imponible_salud = fields.Float('Tope Imponible Salud')

