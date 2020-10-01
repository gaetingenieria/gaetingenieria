from odoo import api, fields, models, tools, _


class hr_contract_type(models.Model):
    _inherit = 'hr.contract.type'
    _description = 'Tipo de Contrato'

    codigo = fields.Char('Codigo')
    as_tipo = fields.Selection([('indefinido', 'Indefinido'), ('plazo_fijo', 'Plazo Fijo')], 'Para contrato', default="indefinido")    
    as_tipo_format = fields.Selection([('indefinido', 'Indefinido'), ('indefinido_auxiliar', 'Indefinido Auxiliar'),('part_time', 'Part Time Extranjero')], 'Para formato de contrato', default="indefinido")