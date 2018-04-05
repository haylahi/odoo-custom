# -*- coding: utf-8 -*-
import logging
import json
import ast
import io
import base64
from openerp import api, fields, models, _


_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    file_factura_json = fields.Binary('Descargar Archivo Sunat')
    factura_binary_fname = fields.Char('Archivo Sunat')
    
    @api.multi
    def compute_round(self, amount):
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        prec = currency.decimal_places
        return round(amount, prec)
    
    @api.multi
    def tax(self, taxids, strtax ):
        tax = taxids.filtered(lambda   r: r.name.startswith(strtax))
        return tax
    
    @api.multi
    def generate_json_file_invoice(self):
        ruta_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.ruta')]).value
        lines = []
        
        if ruta_sunat!='':
            for invoice in self:
                res_partner = self.env['res.partner'].browse(invoice.partner_id)
                num_ruc_company = invoice.company_id.vat
                cc = invoice.journal_id.sequence_id.code
                serie = invoice.journal_id.sequence_id.prefix
                serie = serie[:4]
                number_invoice = invoice.number
                number_invoice = number_invoice[5:]
                namefilejson = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".json"
                 
                _logger.debug('SERA 0 >> %s  ', invoice.partner_id)
                _logger.debug('SERA 1 >> %s  ', invoice.partner_id.website)
                _logger.debug('SERA 2 >> %s  ', invoice.invoice_line_ids)
                
                for line in invoice.invoice_line_ids:
                    _logger.debug('SERA 30 >> %s  ', line.name)
                    _logger.debug('SERA 31 >> %s  ', line.product_id.default_code)
                    _logger.debug('SERA 32 >> %s  ', line.quantity)
                    _logger.debug('SERA 33 >> %s  ', line.price_unit)
                    
                    #tax = line.invoice_line_tax_ids.filtered(lambda   r: r.name.startswith('IGV'))
                    tax = self.tax(line.invoice_line_tax_ids,'IGV 18')
                    taxISC = self.tax(line.invoice_line_tax_ids,'ISC')
                    
                    #_logger.debug('SERA 34 >> %s  ', line.invoice_line_tax_ids.filtered(lambda   r: r.name.startswith('IGV')))
                    _logger.debug('SERA 35 >> %s  ', tax.name)
                    _logger.debug('SERA 36 >> %s  ', tax.amount)
                    
                    #_logger.debug('SERA 34 >> %s  ', tax.description)
                    
                    #Calculos por item:
    
                    #Cod unidade de medida SUNAT - Catalogo 3
                    codUnidadMedida = line.product_id.uom_id.x_code 
    
                    #Cantidad por item
                    quantity = '%.10f' % line.quantity
                    
                    #Descripcion de item
                    desItem = line.product_id.name[:250]
                    
                    #Precio de item por unidad
                    price_unit = '%.10f' % line.price_unit
                    
                    #IGV por Item
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    mtoPrecioVentaItem = (price * line.quantity)
                    mtoIgvItem = (mtoPrecioVentaItem / 100.0) * tax.amount
                    format_mtoIgvItem = '%.2f' % self.compute_round(mtoIgvItem)
                    
                    #Tipo de IGV - Catalogo 7
                    tipAfeIGV = line.x_code_catalog_07.code
                    
                    if taxISC!='':
                        #ISC por Item
                        mtoIscItem = (mtoPrecioVentaItem / 100.0) * taxISC.amount
                        format_mtoIscItem = '%.2f' % self.compute_round(mtoIscItem)
                        
                        #Tipo de ISC - Catalogo 8
                        tipSisISC = line.x_code_catalog_08.code
                    else:
                        format_mtoIscItem = '%.2f' % 0
                        tipSisISC = 0
                    
                    
                    #Precio de venta unitario por item
                    format_mtoPrecioVentaItem = '%.10f' % mtoPrecioVentaItem  
                    
                    #Precio de venta por item
                    format_mtoValorVentaItem = '%.2f' % (mtoPrecioVentaItem + mtoIgvItem)  
                    
                    lines.append({
                                "codUnidadMedida": codUnidadMedida,
                                "ctdUnidadItem":quantity,
                                "codProducto":line.product_id.default_code,
                                "desItem":desItem,
                                "mtoValorUnitario":price_unit,
                                "mtoIgvItem": format_mtoIgvItem,
                                "tipAfeIGV":tipAfeIGV,
                                "tipSisISC":tipSisISC,
                                "mtoIscItem": format_mtoIscItem,
                                "mtoPrecioVentaItem":format_mtoPrecioVentaItem,
                                "mtoValorVentaItem":format_mtoValorVentaItem
                             })
    
                
                #Caculos por totales
                
                #Tipo de usuario - Catalogo 6
                tipDocUsuario = invoice.partner_id.catalog_06_id.code
                
                #Num documento de usuario
                numDocUsuario = invoice.partner_id.vat[:15]
                
                #Razon Social
                if (invoice.partner_id.registration_name != False):
                    rznSocialUsuario = invoice.partner_id.registration_name[:100]
                else:
                    rznSocialUsuario = ''
                
                #Tipo de moneda - Catalogo 2
                tipMoneda = invoice.currency_id.name
                
                #Monto total
                amount_untaxed = '%.2f' % invoice.amount_untaxed
                amount_tax = '%.2f' % invoice.amount_tax
                amount_total = '%.2f' % invoice.amount_total
                
                datos = {
                       "fecEmision": invoice.date_invoice,
                       "tipDocUsuario":tipDocUsuario,
                       "numDocUsuario":numDocUsuario,
                       "rznSocialUsuario":rznSocialUsuario,
                       "tipMoneda":tipMoneda,
                       "mtoOperGravadas": amount_untaxed,
                       "mtoOperInafectas":"0.00",
                       "mtoOperExoneradas":"0.00",
                       "mtoIGV": amount_tax,
                       "mtoImpVenta": amount_total,
                       "lstItems": lines
                      
                    }
                
                with open(ruta_sunat+namefilejson, 'w') as file:
                    json.dump(datos, file,sort_keys=True,separators=(',',':'))
                
                file = open(ruta_sunat+namefilejson, "rb")
                out = file.read()
                file.close()
                invoice.file_factura_json = base64.encodestring(out)
                invoice.factura_binary_fname = namefilejson
                self.write({'factura_binary_fname': namefilejson})
                
                _logger.debug('CreateXYZ3 a %s with ', self._name)
                _logger.debug('Valor a %s with ', invoice.date_invoice)
        else:
            _logger.debug('Verifique el parametro de sistema de la ruta de archivos de Sunat !')
    
    
    @api.multi
    def action_invoice_draft(self):
        res = super(account_invoice, self).action_invoice_draft()
        return res
    
    @api.multi
    def invoice_validate(self):
        _logger.debug('CreateXYZ2 a %s with ', self._name)
        res = super(account_invoice, self).invoice_validate()
        return res
    
    @api.multi
    def generate_sunat_files(self):
        _logger.debug('SERA 0123456789 >> %s  ')
        if ast.literal_eval(self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr')]).value):
                return self.generate_json_file_invoice()