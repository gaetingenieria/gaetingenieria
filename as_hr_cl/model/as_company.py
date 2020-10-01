# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Company(models.Model):
    _inherit = "res.company"

    representante_name = fields.Char('Nombre del Representante legal')
    representante_rut = fields.Char('RUT del Representante legal')
    comuna = fields.Char('Comuna')
    icon_image = fields.Binary(string='Firma Digital')