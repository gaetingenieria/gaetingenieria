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

    employer_id = fields.Many2one('as.hr.employer', string='Empleador',required=True)
    rut = fields.Char(related='employer_id.rut')


# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz

from collections import defaultdict
from contextlib import contextmanager
from itertools import chain
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.hr_payroll.models.hr_work_intervals import WorkIntervals


class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    
    def action_validate(self):
        """
        Try to validate work entries.
        If some errors are found, set `state` to conflict for conflicting work entries
        and validation fails.
        :return: True if validation succeded
        """
        work_entries = self.filtered(lambda work_entry: work_entry.state != 'validated')
        # if not work_entries._check_if_error():
        work_entries.write({'state': 'validated'})
        return True