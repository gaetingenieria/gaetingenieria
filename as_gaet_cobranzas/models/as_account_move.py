# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
      

class AccountInvoice(models.Model):
    _inherit = "account.move"

    as_cont_invoice = fields.Integer(string='Contador de facturas')
    as_invoice_number = fields.Integer(string='Nro. Factura')
    as_date_fiscal = fields.Date(string='Fecha Factura Fiscal')

    def action_post(self):
        res = super(AccountInvoice, self).action_post()
        self.name = self.as_cont_invoice
        return res