# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class LandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    analytic_tag_id = fields.Many2one(
        'account.analytic.tag', string="Analytic tag",
        help="Analytic tag that will be searched. E.g. DIN1")

    def generate_cost_lines(self):
        """Generates the cost lines depending on the landed cost products found
        in the invoices associated with the specified tag."""
        if self.cost_lines:
            raise ValidationError(_("The cost lines were already generated."))

        invoices = self.env['account.move'].search([]).filtered(
            lambda r: self.analytic_tag_id in r.analytic_tag_ids)

        if not invoices:
            raise ValidationError(_(
                "No invoices were found associated with analytic tag."))

        cost_lines = {}
        for line in invoices.mapped('invoice_line_ids'):
            if line.product_id.product_tmpl_id.landed_cost_ok:
                cost_lines.update({
                    line.product_id: cost_lines.get(
                        line.product_id, 0.0) + line.price_unit,
                })

        if not cost_lines:
            raise ValidationError(_(
                "None of the invoices has at least one landed cost product."))

        self.write({
            'cost_lines': [(0, 0, {
                'product_id': product.id,
                'name': product.name or '',
                'split_method': product.product_tmpl_id.split_method_landed_cost or 'equal',
                'price_unit': price,
                'account_id': product.property_account_expense_id.id
                    or product.categ_id.property_account_expense_categ_id.id,
                }) for product, price in cost_lines.items()],
        })


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    new_cost = fields.Float(
        compute='_compute_new_cost',
        help="Former Cost (Per unit) + Additional Landed Cost / Quantity")

    def _compute_new_cost(self):
        """Computes the new cost based on the former cost, additional landed
        cost and quantity."""
        for record in self:
            record.new_cost = (
                record.former_cost + record.additional_landed_cost
                / record.quantity)
