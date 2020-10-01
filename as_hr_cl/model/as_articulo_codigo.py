# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Company(models.Model):
    _name = "as.hr.articulo"

    name = fields.Char('Nombre')
    as_inciso = fields.Integer('Inciso')
    as_articulo= fields.Integer('Artículo')
    as_motivo = fields.Char('Motivo')