# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.order_id.convert_to_company_currency and self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            company = self.env.user.company_id
            currency = self.order_id.pricelist_id.currency_id
            res.update({
                'price_unit': currency._convert(self.price_unit, company.currency_id, company, self.order_id.date_order or fields.Date.today()),
            })
        return res
