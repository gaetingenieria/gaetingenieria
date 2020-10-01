from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
from datetime import date
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone
from datetime import date, datetime, time
from odoo.exceptions import UserError
from itertools import cycle

class employer(models.Model):
    _name='as.hr.employer'
    _description = 'Employer contract'
        
    name = fields.Char(string='Empleador')
    rut = fields.Char(string='RUT')
    address = fields.Char(string='Dirección')
    representante_name = fields.Char('Nombre del Representante legal')
    representante_rut = fields.Char('RUT del Representante legal')
    comuna = fields.Char('Comuna')
    icon_image = fields.Binary(string='Firma Digital')
    icon_logo = fields.Binary(string='Logo')
  

 