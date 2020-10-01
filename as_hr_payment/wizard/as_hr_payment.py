# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class Ahorasoftpaymentslip(models.TransientModel):
    _name = "as.hr.payments"
    _description = "Report payslip Report AhoraSoft"

    payslip_run_id = fields.Many2one('hr.payslip.run', string="Nomina",default=1)
    date = fields.Date('Fecha Pago', default=fields.Date.context_today)
    payment_method_id = fields.Many2one('account.payment.method', string='Forma de Pago', required=True)
    as_agrupar = fields.Boolean( string="Agrupar Pagos Transferencia")
    slip_bank_ids = fields.Many2many('hr.payslip', string='Con Cuenta Bancaria')
    slip_ids = fields.Many2many('as.hr.payments.line', string='Sin Cuenta Bancaria')
    bank_journal_id = fields.Many2one('account.journal', string='Diario (transferencia)', domain="[('type', 'in', ['cash', 'bank'])]",required=True)


    @api.onchange('payment_method_id')
    def get_forma_pago(self):
        for slip in self.slip_ids:
            slip.payment_method_id =self.payment_method_id

    def action_process_payments(self):
        method_pago_m = self.env['account.payment.method'].sudo().search([('code', '=', 'manual')],limit=1)
        method_pago = self.env['account.payment.method'].sudo().search([('code', '=', 'TRANS')],limit=1)
        payments_ids=[]
        if self.as_agrupar:
            slip_manual_ids=[]
            for slip in self.slip_bank_ids:
                vals={
                'payment_method_id': method_pago.id,
                'payment_type': 'outbound',
                'amount': slip.net_wage,
                'as_type_operation': 'nomina',
                'partner_id': slip.employee_id.user_id.partner_id.id,
                'journal_id': self.bank_journal_id.id,
                'slip_ids': [slip.id],
                'slip_id': slip.id,
                'partner_type': 'supplier',
                }
                payment = self.env['account.payment'].create(vals)
                payments_ids.append(payment.id)
            total = 0.0 
            for slip in self.slip_ids.slip_ids:
                slip_manual_ids.append(slip.id)
                total += slip.net_wage
            vals={
            'payment_method_id': method_pago_m.id,
            'payment_type': 'outbound',
            'amount': total,
            'as_type_operation': 'procesamiento',
            'partner_id': self.payslip_run_id.company_id.partner_id.id,
            'journal_id': self.bank_journal_id.id,
            'partner_type': 'supplier',
            'slip_ids':slip_manual_ids,
            }
            payment2=self.env['account.payment'].create(vals)
            payments_ids.append(payment2.id)
            self.payslip_run_id.update({'payment_ids':payments_ids})
        else:
            slip_manual_ids=[]
            total = 0.0 
            for slip in self.slip_bank_ids:
                total += slip.net_wage 
                slip_manual_ids.append(slip.id)
            for slip in self.slip_ids.slip_ids:
                slip_manual_ids.append(slip.id)
                total += slip.net_wage
            vals={
            'payment_method_id': method_pago_m.id,
            'payment_type': 'outbound',
            'amount': total,
            'as_type_operation': 'procesamiento',
            'partner_id': self.payslip_run_id.company_id.partner_id.id,
            'journal_id': self.bank_journal_id.id,
            'partner_type': 'supplier',
            'slip_ids':slip_manual_ids,
            }
            payment2=self.env['account.payment'].create(vals)
            payments_ids.append(payment2.id)
            self.payslip_run_id.update({'payment_ids':payments_ids})

class AhorasoftpaymentslipLine(models.TransientModel):
    _name = "as.hr.payments.line"
    _description = "Report payslip Report AhoraSoft"

    slip_ids = fields.Many2one('hr.payslip', string='Sin Cuenta Bancaria',domain=[('as_cuenta','=',False)])
    payment_method_id = fields.Many2one('account.payment.method', string='Forma de Pago', required=True)

