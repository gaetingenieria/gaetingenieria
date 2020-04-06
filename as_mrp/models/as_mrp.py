# -*- coding: utf-8 -*-

import datetime
from collections import defaultdict
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import date_utils, float_round, float_is_zero

import logging
_logger = logging.getLogger(__name__)
#clase heredada de purchase order para agregar funciones de creacion de facturas y campos adicionales


class MrpProduction(models.Model):
    ''' Manufacturing Orders '''
    _inherit = 'mrp.production'

    def _get_move_raw_values(self, bom_line, line_data):
        quantity = line_data['qty']
        # alt_op needed for the case when you explode phantom bom and all the lines will be consumed in the operation given by the parent bom line
        alt_op = line_data['parent_line'] and line_data['parent_line'].operation_id.id or False
        source_location = self.location_src_id
        data = {
            'sequence': bom_line.sequence,
            'name': self.name,
            'reference': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            'bom_line_id': bom_line.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': bom_line.product_id.id,
            'product_uom_qty': quantity,
            'as_stock_actual': float(self._compute_amount(bom_line.product_id.id,self.picking_type_id.default_location_dest_id.id)),
            'product_uom': bom_line.product_uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.with_context(force_company=self.company_id.id).property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': bom_line.product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'state': 'draft',
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate_cancel': self.propagate_cancel,
        }
        return data

    @api.model
    def _compute_amount(self,product_id,location_id):
        cantidad = 0.0
        self._cr.execute('''
            SELECT CASE WHEN ( ( SELECT spt.CODE FROM stock_picking_type spt WHERE spt.id = sm.picking_type_id ) = 'outgoing' ) OR ( sm.location_id = %s ) THEN - SUM( sm.product_qty ) ELSE SUM( sm.product_qty ) END AS cantidad, CASE WHEN ( sm.location_id = %s ) and ( sm.location_dest_id = %s ) THEN SUM( sm.product_qty ) ELSE 0 END AS cantidad2, sm.location_id  FROM stock_move as sm  WHERE sm.state IN ( 'done' ) AND ( sm.location_id = %s OR sm.location_dest_id = %s ) AND ( ( sm.date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT' ) :: date ) <= now() AND sm.product_id = %s GROUP BY sm.location_id, sm.location_dest_id, sm.picking_type_id
            ''',([location_id,location_id,location_id,location_id,location_id,product_id]))
        res = self._cr.fetchall()
        if res != []:
            cantidad = sum((x[0] + x[1]) for x in res)
        return float(cantidad)
            
class asMRP(models.Model):
    _inherit = 'stock.move'

    as_stock_actual = fields.Float(string='Stock actual')
