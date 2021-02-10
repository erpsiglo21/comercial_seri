# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleUploadXml(models.TransientModel):
    _name = 'sale.upload.xml'
    _description = 'Puchase Order from Mercado Publico'

    xml_file = fields.Binary(
        string='XML File',
        attachment=False,
        help='Upload the XML File in this holder'
    )
    filename = fields.Char(
        string='File Name'
    )

    def confirm(self, ret=False):
        raise UserError("No se pudo cargar libreria lxml")
    
