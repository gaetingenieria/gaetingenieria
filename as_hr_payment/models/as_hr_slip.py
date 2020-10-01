from pytz import timezone
from datetime import date, datetime, time

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    payment_id = fields.Many2one('account.payment', string="Pago Asociado")
    as_cuenta = fields.Boolean( string="Agrupar Pagos Transferencia", compute='_compute_account_bank')
    as_cuenta = fields.Boolean( string="Agrupar Pagos Transferencia", compute='_compute_account_bank')

    def _compute_account_bank(self):
        for slips in self:
            if slips.employee_id.user_id.partner_id.bank_ids:
                self.as_cuenta= True
            else:
                self.as_cuenta= False

    def _compute_basic_net(self):
        for payslip in self:
            payslip.basic_wage = payslip._get_salary_line_total('SUELDO')
            payslip.net_wage = payslip._get_salary_line_total('LIQ')


class hr_payslip_run(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'

    @api.depends('as_paid','payment_ids.state')
    def _get_state_paid_nomina(self):
        for run in self:
            if run.state == 'close':
                pagada =False
                total_pagos = len(run.payment_ids)
                contador_pagados = 0 
                for nomina in run.payment_ids:
                    if nomina.state == 'posted':
                        contador_pagados+=1
                if contador_pagados == total_pagos:
                    run.update({'state':'paid','as_paid':True})
                else:
                    run.update({'state':'close','as_paid':False})
            else:
                run.as_paid=False

    state = fields.Selection(selection_add=[('paid', 'Pagada')])
    payment_ids =  fields.One2many('account.payment', 'nomina_id',string='Pagos Realizados')
    as_paid = fields.Boolean( string="Nomina Pagada", store=True, readonly=True, compute='_get_state_paid_nomina', tracking=4)

    def action_payslip_paid(self):
        self.ensure_one()
        bank=[]
        out_bank=[]
        for slips in self.slip_ids:
            if slips.employee_id.user_id.partner_id.bank_ids:
                bank.append(slips.id)
            else:
                vals={
                    'slip_ids':slips.id
                }
                out_bank.append(vals)
        action = self.env.ref('as_hr_payment.as_action_as_hr_payment_wiz').read()[0]
        action.update({
            'context': {
                'default_payslip_run_id': self.id,
                'default_as_agrupar': True,
                'default_slip_bank_ids': bank,
                'default_slip_ids': out_bank,
               
            },
        })
        return action  

