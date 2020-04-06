# -*- coding: utf-8 -*-

import base64
import logging
import tempfile

from odoo import _, api, models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'

    as_price_line = fields.One2many('as.product.price', 'as_product_id', string='Price Lines', copy=True, auto_join=True)

    
class as_product_price(models.Model):
    _name = 'as.product.price'

    name = fields.Char(string='Proveedor')
    as_precio_proveedor = fields.Float(string='Precio de Compra')
    as_precio_nimax = fields.Float(string='Precio NIMAX')
    as_utilidad = fields.Float(string='Utilidad')
    as_descuento = fields.Float(string='Descuento')
    as_precio_final = fields.Float(string='Precio de Venta Final')
    as_product_id = fields.Many2one('product.product', string='Product ID',  required=True, ondelete='cascade', index=True, copy=False)