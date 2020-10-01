# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
      

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _editable_fecha_pedido(self):
        editable = bool(self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_fechas_pedido_editable'))
        self.as_fecha_Editable =  editable
        return editable

    date_order = fields.Datetime(string='Fecha del pedido', readonly=False,default=fields.Datetime.now)
    as_fecha_Editable = fields.Boolean(string='Fechas Editables en Pedido de Venta', compute='_editable_fecha_pedido',default='_editable_fecha_pedido')

