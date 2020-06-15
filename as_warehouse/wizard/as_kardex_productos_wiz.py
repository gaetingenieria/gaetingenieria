# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models

class as_kardex_productos_wiz(models.TransientModel):
    _name="as.kardex.productos.wiz"
    _description = "Warehouse Reports by AhoraSoft"
    
    start_date = fields.Date('Desde la Fecha', default=fields.Date.context_today)
    end_date = fields.Date('Hasta la Fecha', default=fields.Date.context_today)
    as_almacen = fields.Many2many('stock.location', string="Almacen", domain="[('usage', '=', 'internal')]")
    as_productos = fields.Many2many('product.product', string="Productos")
    category_ids = fields.Many2many('product.category', string="Categoria de Productos")
    as_consolidado = fields.Boolean(string="Consolidado", default=False)
    as_categ_levels = fields.Integer(string="Niveles de categorias", help=u"Debe ser un entero igual o mayor a 1", default=2)

    def export_xls(self):
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('as_warehouse.kardex_productos_xlsx').report_action(self, data=data)