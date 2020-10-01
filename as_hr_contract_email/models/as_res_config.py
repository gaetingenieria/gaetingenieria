from odoo import fields,models,api, _

class res_config(models.TransientModel): 
    _inherit='res.config.settings'
        
    as_days_contract = fields.Float(string='Dias para notificar contratos a caducar')
    
    @api.model
    def get_values(self):
        res = super(res_config, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(as_days_contract = float(params.get_param('as_hr_contract_email.as_days_contract',default=5)))
        return res
    
    def set_values(self):
        super(res_config,self).set_values()
        ir_parameter = self.env['ir.config_parameter'].sudo()        
        ir_parameter.set_param('as_hr_contract_email.as_days_contract', self.as_days_contract)
       