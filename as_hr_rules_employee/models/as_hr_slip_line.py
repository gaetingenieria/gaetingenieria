# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    employee_id = fields.Many2one(related='slip_id.employee_id', readonly=True, store=True)
    run_id = fields.Many2one(related='slip_id.payslip_run_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', related='run_id.state')