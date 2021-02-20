# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import re
import logging
import xmltodict
import base64
import collections
from lxml import etree

_logger = logging.getLogger(__name__)

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
        context = dict(self._context or {})
        xmlfile = base64.b64decode(self.xml_file).decode('UTF-8').replace('<?xml version="1.0"?>','').replace('<?xml version="1.0" ?>','')
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.XML(xmlfile, parser)
        # Limpia namespace
        for elem in xml.getiterator():
            elem.tag = etree.QName(elem).localname
        # Elimina declaraciones namespace no utilizadas
        etree.cleanup_namespaces(xml)
        # Obtiene las ordenes a procesar
        ordenes = xml.xpath('OrdersList/Order')
        aCrear = []
        errores = []
        for orden in ordenes:
            # Recupera la empresa a la cual va dirigida la orden
            company_rut = orden.xpath('OrderHeader/OrderParty/SellerParty/PartyID/Ident')[0].text.replace('.', '')
            company_id = self.env['res.company'].search([('vat', '=', company_rut)], limit=1)
            if not company_id:
                errores.append('No se pudo encontrar la informacion para la compañia con RUT ' + company_rut)
            # Recupera el cliente
            partner_rut = orden.xpath('OrderHeader/OrderParty/BuyerParty/PartyID/Ident')[0].text.replace('.', '')
            partner_id = self.env['res.partner'].search([('vat', '=', partner_rut)], limit=1)
            if not partner_id:
                errores.append('No se encontro la informacion del cliente RUT ' + partner_rut)
            # Recupera el detalle de la orden
            lineas = orden.xpath('OrderDetail/ListOfItemDetail/ItemDetail')
            detalle = []
            for linea in lineas:
                # Recupera el sku
                sku = re.sub('(\(|\))', '', re.findall('^\([0-9]+\)', linea.xpath('BaseItemDetail/ItemIdentifiers/ItemDescription')[0].text)[0])
                # Verifica si el sku existe
                product_id = self.env['product.product'].search([('default_code','=', sku)], limit=1)
                if not product_id:
                    errores.append("El sku " + sku + " no esta definido")
                # Recupera la cantidad ordenada
                cantidad = linea.xpath('BaseItemDetail/TotalQuantity/QuantityValue')[0].text
                # Recupera el precio
                precio = linea.xpath('PricingDetail/ListOfPrice/Price/UnitPrice/UnitPriceValue')[0].text
                # Agrega al detalle
                detalle.append({
                    'product_id': product_id,
                    'qty_ordered': cantidad,
                    'price': precio
                })
            # Agrega a las ordenes a crear
            aCrear.append({
                'company_id': company_id,
                'partner_id': partner_id,
                'order_lines': detalle
            })
        if not errores:
            try:
                self.env['sale.sale.order'].create(aCrear)
            except:
                raise UserError('Error al generar las ordenes de venta')
        else:
            elError = "Se han generado los siguientes errores:\n"
            for error in errores:
                elError = elError + "- " + error + "\n"
            raise UserError(elError)
