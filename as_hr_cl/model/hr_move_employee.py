from odoo import api, fields, models, tools, _


class hr_afp(models.Model):
    _name = 'hr.move.employee'
    _description = 'movimiento de personal'

    codigo = fields.Char('Codigo', required=True)
    name = fields.Char('Nombre', required=True)
  