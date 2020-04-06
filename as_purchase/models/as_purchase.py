# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from dateutil import relativedelta
from odoo.exceptions import UserError

from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase
#clase heredada de purchase order para agregar funciones de creacion de facturas y campos adicionales
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    as_stock_actual = fields.Float(string='Stock actual',readonly=True)
    as_procesar = fields.Boolean(string='Comprar', default=False)

    def _create_stock_moves(self, picking):
        values = []
        for line in self.filtered(lambda l: not l.display_type):
            for val in line._prepare_stock_moves(picking):
                if line.order_id.user_has_groups('as_purchase.group_purchase_line_selected'):
                    if line.as_procesar == True:
                        values.append(val)
                else:
                    values.append(val)
        return self.env['stock.move'].create(values)
        
    @api.onchange('product_id')
    def _compute_qty_receiveed(self):
        cantidad = 0.0 
        for line in self:
            if line.order_id.picking_type_id and line.product_id:
                location_id = line.order_id.picking_type_id.default_location_dest_id.id
                self._cr.execute('''
                SELECT CASE WHEN ( ( SELECT spt.CODE FROM stock_picking_type spt WHERE spt.id = sm.picking_type_id ) = 'outgoing' ) OR ( sm.location_id = %s ) THEN - SUM( sm.product_qty ) ELSE SUM( sm.product_qty ) END AS cantidad, CASE WHEN ( sm.location_id = %s ) and ( sm.location_dest_id = %s ) THEN SUM( sm.product_qty ) ELSE 0 END AS cantidad2, sm.location_id  FROM stock_move as sm  WHERE sm.state IN ( 'done' ) AND ( sm.location_id = %s OR sm.location_dest_id = %s ) AND ( ( sm.date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT' ) :: date ) <= now() AND sm.product_id = %s GROUP BY sm.location_id, sm.location_dest_id, sm.picking_type_id 
                ''',([location_id,location_id,location_id,location_id,location_id,line.product_id.id]))
                # array = sum((x[0] + x[1]) for x in self._cr.fetchall())
                res = self._cr.fetchall()
                if res != []:
                    cantidad = sum((x[0] + x[1]) for x in res)
            line.as_stock_actual = cantidad