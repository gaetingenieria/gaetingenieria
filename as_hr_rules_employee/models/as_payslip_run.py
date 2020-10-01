from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from time import mktime
from odoo.exceptions import UserError, RedirectWarning, ValidationError, MissingError
import time
import calendar
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from datetime import datetime, timedelta

class hr_payslip_run(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'

    def action_validate(self):
        res = super(hr_payslip_run, self).action_validate()  
        for slip in self.slip_ids:
            for rules in slip.employee_id.salary_rule_id:
                rules._get_line_control()
        return res

