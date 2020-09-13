# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, time
from odoo.tools.safe_eval import safe_eval
import logging
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError

#from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class asSaleOrderWizard(models.Model):
    _name = 'as.planilla.general'
    _description = 'Planilla general'

    as_partner_id = fields.Many2one('res.partner', 'Cliente')
    # as_sale = fields.Many2one('sale.order', 'Sale Order')

    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'res.partner'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('as_gaet_cobranzas.report_planilla_gaet').report_action(self.as_partner_id, data=datas)
