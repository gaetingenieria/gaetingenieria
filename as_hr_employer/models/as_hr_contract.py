from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
class hr_contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    employer_id = fields.Many2one('as.hr.employer', string='Empleador')

    @api.constrains('employee_id', 'state', 'kanban_state', 'date_start', 'date_end')
    def _check_current_contract(self):
        """ Two contracts in state [incoming | open | close] cannot overlap """
        for contract in self.filtered(lambda c: c.state not in ['draft', 'cancel'] or c.state == 'draft' and c.kanban_state == 'done'):
            domain = [
                ('id', '!=', contract.id),
                ('employer_id', '=', contract.employer_id.id),
                ('employee_id', '=', contract.employee_id.id),
                # '|',
                #     ('state', 'in', ['open', 'close']),
                #     '&',
                #         ('state', '=', 'draft'),
                #         ('kanban_state', '=', 'done') # replaces incoming
            ]

            if not contract.date_end:
                start_domain = []
                end_domain = ['|', ('date_end', '>=', contract.date_start), ('date_end', '=', False)]
            else:
                start_domain = [('date_start', '<=', contract.date_end)]
                end_domain = ['|', ('date_end', '>', contract.date_start), ('date_end', '=', False)]

            domain = expression.AND([domain])
            if self.search_count(domain):
                raise ValidationError(_('An employee can only have one contract at the same time. (Excluding Draft and Cancelled contracts)'))

from odoo.osv import expression