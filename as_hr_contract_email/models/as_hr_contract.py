from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
from datetime import date
from dateutil.relativedelta import relativedelta
class hr_contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    @api.model
    def update_state(self):
        #envio de correo para notificar con 5 dias de anticipacion vencimiento de contrato
        # from_to = self.employee_id.address_id.email
        mail_template = self.env.ref('as_hr_contract_email.email_contract_edi_hr_2')
        lang = self.env.context.get('lang')
        num = int(float(self.env['ir.config_parameter'].sudo().get_param('as_hr_contract_email.as_days_contract')))
        desde = fields.Date.to_string(date.today() - relativedelta(days=num))
        hasta = fields.Date.to_string(date.today() + relativedelta(days=1))
        contratos_vencer = self.search([
            ('state', '=', 'open'),
            '&',
            ('date_end', '>=', desde),
            ('date_end', '<',  hasta),
        ])
        for contract in contratos_vencer:
            from_name = self.env.user.company_id.name 
            body = 'Hola '+str(from_name)+'!! <br/><br/><br/>Los siguientes <b>contratos</b> estan por Caducar:<br/>'
            from_to = contract.employee_id.address_id.email 
            body += '<b style="color:blue">'+contract.name+'</b><br/>' 
            email_values = {
                'email_to': from_to,
            }
            mail_template.send_mail(contract.id, force_send=True, email_values=email_values)
        res = super(hr_contract, self).update_state()
        return res
