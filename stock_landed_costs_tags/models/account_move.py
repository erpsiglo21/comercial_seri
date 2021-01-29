# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string='Analytic Tags',
        help="Analytic tags to be associated with this invoice.")

    @api.onchange("analytic_tag_ids")
    def _onchange_analytic_tag_ids(self):
        """Assigns the analytic tag to each invoice line."""
        if self.invoice_line_ids:
            for line in self.invoice_line_ids:
                line.analytic_tag_ids = self.analytic_tag_ids.ids


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Assigns the analytic tag to each invoice line."""
        if self.move_id.analytic_tag_ids:
            self.analytic_tag_ids = self.move_id.analytic_tag_ids.ids
        return super(AccountMoveLine, self)._onchange_product_id()
