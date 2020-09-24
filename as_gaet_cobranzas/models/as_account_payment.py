# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
      

class AccountInvoice(models.Model):
    _inherit = "account.payment"

    payment_acquirer_id = fields.Many2one('as.payment.acquirer', string='Método de Pago')
    as_lugar_retiro = fields.Char('Lugar de Retiro')
    as_retira = fields.Char('Retira')
    as_ciudad = fields.Char('Ciudad')
    #campos para vista desglose de pago
    as_iva_retenido = fields.Char('Iva Retenido')
    amount_untaxed = fields.Monetary(string='Monto Base', related="invoice_ids.amount_untaxed")
    amount_total = fields.Monetary(string='Valor Total', related="invoice_ids.amount_total")
    amount_retencion = fields.Monetary(string='Retencion', related="invoice_ids.amount_retencion")
    amount_neto = fields.Monetary(string='Valor Neto', related="invoice_ids.amount_neto")
    amount_impuesto = fields.Monetary(string='IVA', related="invoice_ids.amount_tax")
    as_iva = fields.Monetary(string='IVA', related="invoice_ids.amount_total")
    invoice_date = fields.Date(string='EEPP Fecha' ,related="invoice_ids.invoice_date")
    as_invoice_number = fields.Integer(string='EEPP Nro.', related="invoice_ids.as_invoice_number")


    @api.model
    def _compute_payment_amount(self, invoices, currency, journal, date):
        result = super(AccountInvoice,self)._compute_payment_amount(invoices, currency, journal, date)
        for inv in invoices:
            if inv.as_retencion:
              result = inv.amount_total  
        return result
