# -*- coding: utf-8 -*-
import logging
import json
from openerp import api, fields, models, _


_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def action_invoice_draft(self):
        for invoice in self:
            res_partner = self.env['res.partner'].browse(invoice.partner_id)
             
            _logger.debug('SERA 0 >> %s  ', invoice.partner_id)
            _logger.debug('SERA 1 >> %s  ', invoice.partner_id.website)

            
            datos = {
                   "fecEmision": invoice.date_invoice,
                   "tipDocUsuario":invoice.partner_id.catalog_06_id.code,
                   "numDocUsuario":invoice.partner_id.vat,
                   "rznSocialUsuario":invoice.partner_id.registration_name,
                   "tipMoneda":invoice.currency_id.name,
                   "mtoOperGravadas":invoice.amount_untaxed,
                   "mtoOperInafectas":"0.00",
                   "mtoOperExoneradas":"0.00",
                   "mtoIGV":invoice.amount_tax,
                   "mtoImpVenta":invoice.amount_total,
                   "lstItems": [
                         {
                            "codUnidadMedida": "NIU",
                            "ctdUnidadItem":"2",
                            "codProducto":"COD_01",
                            "codProductoSUNAT":"",
                            "desItem":"DETALLE DEL PRODUCTO 1",
                            "mtoValorUnitario":"5.00",
                            "mtoDsctoItem":"0.00",
                            "mtoIgvItem":"1.80",
                            "tipAfeIGV":"10",
                            "mtoIscItem":"0.00",
                            "tipSisISC":"01",
                            "mtoPrecioVentaItem":"10.00",
                            "mtoValorVentaItem":"11.80"
                         }, {
                            "codUnidadMedida": "NIU",
                            "ctdUnidadItem":"2",
                            "codProducto":"COD_02",
                            "codProductoSUNAT":"",
                            "desItem":"DETALLE DEL PRODUCTO 2",
                            "mtoValorUnitario":"5.00",
                            "mtoDsctoItem":"0.00",
                            "mtoIgvItem":"1.80",
                            "tipAfeIGV":"10",
                            "mtoIscItem":"0.00",
                            "tipSisISC":"01",
                            "mtoPrecioVentaItem":"10.00",
                            "mtoValorVentaItem":"11.80"
                         }
                   ]
                }
            
            with open('D:\\data0\\facturador\\DATA\\datos.json', 'w') as file:
                json.dump(datos, file,sort_keys=True,separators=(',',':'))
            
            _logger.debug('CreateXYZ3 a %s with ', self._name)
            _logger.debug('Valor a %s with ', invoice.date_invoice)
            res = super(account_invoice, self).action_invoice_draft()
            return res
    
    @api.multi
    def invoice_validate(self):
        _logger.debug('CreateXYZ2 a %s with ', self._name)
        res = super(account_invoice, self).invoice_validate()
        return res