from odoo import fields, models

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    l10n_cl_xml = fields.Text(string='XML DTE')