# -*- encoding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError
import re
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_document(self):
        if self.l10n_latam_identification_type_id.name in ["RUT","RUN"]:
            try:
                elRut = self.vat
                laUrl = "http://api.konos.cl:8000/sii/index.php?id=%s" % elRut
                response = requests.get(laUrl,params="nombre")
            except Exception:
                reponse={status_code:404}

            if response and response.status_code!=200:
                raise UserError(u"Error al invocar el servicio, intente más tarde")
            else:
                vals = response.text
                if len(vals)>40:
                    csx_nombre = self.find_between_r( vals, "[nombre] => ", "[resolucion]" ).rstrip()
                    csx_correoDTE = self.find_between_r( vals, "[correo_dte] => ", "[url]" ).rstrip()
                    csx_web = self.find_between_r( vals, "[url] => ", "[fcreado]" )
                    csx_pais_id = self.env['res.country'].search([("code","=", 'CL')], limit=1)
                    csx_dir = self.find_between_r( vals, "[calle] => ", "[numero]" ).rstrip() + " " + self.find_between_r( vals, "[numero] => ", "[bloque]" ).rstrip()
                    csx_dir2 = self.find_between_r( vals, "[bloque] => ", "[depto]" ).rstrip() + " " + self.find_between_r( vals, "[depto] => ", "[villa]" ).rstrip()
                    csx_comuna = self.find_between_r( vals, "[comuna] => ", "[region]" ).rstrip().lstrip()
                    if len(csx_nombre) > 0:
                        self.name = csx_nombre
                    if len(csx_correoDTE) > 0:
                        self.l10n_cl_dte_email = csx_correoDTE
                    if len(csx_web) > 0:
                        self.website = csx_web
                    self.country_id = csx_pais_id
                    self.company_type="company"
                    if len(csx_dir) > 1:
                        self.street = csx_dir
                    if len(csx_dir2) > 1:
                        self.street2 = csx_dir2
        else:
            raise UserError("El tipo de documento de identificacion no acepta está operacion")

    def find_between_r(self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""