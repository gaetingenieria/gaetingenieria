import re
import logging
from pytz import timezone
from datetime import date, datetime, time
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    salary_rule_id = fields.Many2many('hr.employee.rules', string='Rules', readonly=True)