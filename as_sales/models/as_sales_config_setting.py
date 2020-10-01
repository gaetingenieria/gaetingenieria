# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    as_fechas_pedido_editable = fields.Boolean('Fecha de Pedido No Editable', help='Cambia de estado editable la numeracion interna de ventas', default=False)
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['as_fechas_pedido_editable'] = bool(self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_fechas_pedido_editable'))
       
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('res_config_settings.as_fechas_pedido_editable', self.as_fechas_pedido_editable)
        super(ResConfigSettings, self).set_values()