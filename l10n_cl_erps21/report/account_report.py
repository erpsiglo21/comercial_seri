# -*- coding: utf-8 -*-

from odoo import api, models

class ReportInvoiceWithReceiptData(models.AbstractModel):
    _name = 'report.l10n_cl_erps21.report_invoice_with_receipt_data'
    _description = 'Account report with receipt data'
    _inherit = 'report.account.report_invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        rslt = super()._get_report_values(docids, data)
        rslt['report_type'] = data.get('report_type') if data else ''
        return rslt
