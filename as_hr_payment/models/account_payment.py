# -*- coding: utf-8 -*-

from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode
from odoo import api, exceptions, fields, models, _
from odoo.addons import decimal_precision as dp
import logging
from odoo.exceptions import UserError
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class AsAccountPayment(models.Model):
    _inherit = "account.payment"

    as_type_operation = fields.Selection([('proveedor', 'Proveedor'), ('nomina', 'Pago de Nomina'), ('procesamiento', 'Pago de Procesamiento de Nomina')], string="Tipo de Operación", default='proveedor')
    slip_id = fields.Many2one('hr.payslip', string='Pay Slip', ondelete='cascade', help="Payslip")
    payslip_run_id = fields.Many2one('hr.payslip.run', string="Nomina")
    nomina_id = fields.Many2one('hr.payslip.run', string="Nomina relacional")
    slip_ids = fields.One2many('hr.payslip', 'payment_id', string='Pay Slip', ondelete='cascade', help="Payslip")

    @api.onchange('slip_id','payslip_run_id')
    def _compute_qty_receiveed(self):
        total=0
        if self.slip_id:
            self.slip_ids = self.slip_id.ids
        if self.payslip_run_id:
            self.slip_ids = self.payslip_run_id.slip_ids.ids
        for slip in self.slip_ids:
            for rule in slip.line_ids:
                if rule.code == 'LIQ':
                    total+= rule.total
        self.amount= total


    def post(self):
        res = super(AsAccountPayment, self).post()
        if self.slip_ids:
            for slip in self.slip_ids:
                nomina = slip.payslip_run_id
                if nomina.state == 'close':
                    pagada =False
                    total_pagos = len(nomina.payment_ids)
                    contador_pagados = 0 
                    for payment in nomina.payment_ids:
                        if nomina.state == 'posted':
                            contador_pagados+=1
                    if contador_pagados == total_pagos:
                        nomina.update({'state':'paid','as_paid':True})
        return res