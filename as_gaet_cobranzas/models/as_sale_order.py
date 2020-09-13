# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
      

class SaleOrder(models.Model):
    _inherit = "sale.order"

    as_retencion = fields.Many2one('as.retencion', string='Retención')
    as_medio_pago = fields.Many2one('as.medio.pago', string='Medio de Pago ')
    as_date_fiscal = fields.Date(string='Fecha Factura Fiscal')
    as_cont_invoice = fields.Integer(string='Contador de facturas')
    as_tipo_garantia = fields.Char(string='Tipo de Garantia')
    as_numeracion_interna = fields.Char('Numeracion Interna', help=u'Numeración interna de ventas confirmadas.', copy=False)
    as_type_retencion = fields.Selection(selection=[('before', 'Antes de Retencion'),('after', 'Despues de Retencion')], string='Calculo de IVA',default="before")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        self.as_cont_invoice = self.as_cont_invoice + 1
        invoice_vals['as_cont_invoice'] = self.as_cont_invoice
        return invoice_vals

    def action_confirm(self):
        result = super(SaleOrder,self).action_confirm()
        if not self.as_numeracion_interna:
            self.as_numeracion_interna = self.env['ir.sequence'].next_by_code('sale.order.interna') or 'New'
        return result


class AsRetencion(models.Model):
    _name="as.retencion"
    _description = 'Modelo de porcenyaje de retencion'
    
    name = fields.Char(string='Nombre')
    as_porcentaje = fields.Float(string='(%)')
    as_tope = fields.Float(string='Tope de Retención')

class MedioPago(models.Model):
    _name="as.medio.pago"
    _description = 'Medio de Pago'
    
    name = fields.Char(string='Nombre')
