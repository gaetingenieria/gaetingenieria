# -*- coding: utf-8 -*-

from odoo import api, models


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    # @api.multi
    def action_show_price_provider(self):
        self.ensure_one()
        context = {"form_view_ref": "as_promociones.as_product_product_form_price_provider"}
        return {
            'name': self.product_id.name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.product',
            'res_id': self.product_id.id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }
