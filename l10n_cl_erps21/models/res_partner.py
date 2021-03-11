# -*- encoding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError
import re
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_document(self):
        return True
