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
    as_iva_retenido = fields.Char('Iva Retenido')
    amount_total = fields.Monetary(string='Valor Total', related="invoice_ids.amount_total")
    invoice_date = fields.Date(string='F. Factura' ,related="invoice_ids.invoice_date")
    as_invoice_number = fields.Integer(string='Nro. Factura', related="invoice_ids.as_invoice_number")

    @api.model
    def _compute_payment_amount(self, invoices, currency, journal, date):
        result = super(AccountInvoice,self)._compute_payment_amount(invoices, currency, journal, date)
        for inv in invoices:
            if inv.as_retencion:
              result = inv.amount_total  
        return result
