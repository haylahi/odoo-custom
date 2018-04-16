# -*- coding: utf-8 -*-
import logging
import json
import ast
import io
import base64
import os.path
import suds
from openerp import api, fields, models, _
from suds.client import Client
from suds.plugin import MessagePlugin
from lxml import etree
from lxml.etree import Element, SubElement


#from pysimplesoap.client import SoapClient

_logger = logging.getLogger(__name__)

xsdpath = os.path.dirname(os.path.realpath(__file__)).replace('/models','/static/xsd/ver_1_0/maindoc')


class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        _logger.debug('Cambia namespace')
        soap_env_parent = context.envelope
        #soap_env_parent.set('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
        
        #modify this line to reliably find the "recordReferences" element
        #context.envelope[1].setPrefix('SOAP-ENV')
        #context.envelope[1][0].setPrefix('nsenzito0')
        #context.envelope[1][0][0].setPrefix('nsricardo0')

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    file_factura_json = fields.Binary('Descargar Archivo Sunat')
    factura_binary_fname = fields.Char('Archivo Sunat')
    
    file_factura_xml_send = fields.Binary('Descargar Archivo Sunat')
    factura_binary_fname_xml_send = fields.Char('Archivo Sunat')
    
    file_factura_zip = fields.Binary('Respuesta Sunat')
    factura_binary_fname_zip = fields.Char('Archivo ZIP Sunat')
    file_factura_xml = fields.Binary('Respuesta Sunat')
    factura_binary_fname_xml = fields.Char('Archivo XML Sunat')
    file_factura_cdr = fields.Binary('Respuesta Sunat')
    factura_binary_fname_cdr = fields.Char('Archivo CDR Sunat')
    file_factura_pdf = fields.Binary('Respuesta Sunat')
    factura_binary_fname_pdf = fields.Char('Archivo PDF Sunat')
    
    
    
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
                self.write({'state': 'send'})
                
                _logger.debug('CreateXYZ3 a %s with ', self._name)
                _logger.debug('Valor a %s with ', invoice.date_invoice)
        else:
            _logger.debug('Verifique el parametro de sistema de la ruta de archivos de Sunat !')
            
    
    
    @api.multi
    def generate_xml_invoice_10(self):
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
                #number_invoice = number_invoice[5:]
                #namefilexml = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".xml"
                namefilexml = "20378890161-01-F933-5883.xml"
                 
                _logger.debug('INVOICE 1.0 >> %s  ', invoice.partner_id)
                
                #with open(ruta_sunat+namefilexml, 'w') as file:
                    #json.dump(datos, file,sort_keys=True,separators=(',',':'))
                
                if os.path.isfile(ruta_sunat+namefilexml):
                    file = open(ruta_sunat+namefilexml, "rb")
                    out = file.read()
                    file.close()
                    _logger.debug('XML to %s >> ', out)
                    invoice.file_factura_xml_send = base64.encodestring(out)
                    invoice.factura_binary_fname_xml_send = namefilexml
                    self.write({'factura_binary_fname_xml_send': namefilexml})
                    
                    #Produccion
                    #client = Client(url='https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl',plugins=[MyPlugin()])

                    #Pruebas
                    client = Client(url='https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl',plugins=[MyPlugin()])
                    
                    #auth = client.factory.create('Header')
                    #auth.token = 'xxx'
                    #client.set_options(soapheaders=auth)
                    
                    security =  suds.wsse.Security()
                    token =  suds.wsse.UsernameToken('20378890161MODDATOS', 'moddatos')
                    #token.setnonce('<INSERT_YOUR_NONCE>') # token.setonce() didn't work for me
                    #token.setcreated()
                    security.tokens.append(token)
                    client.set_options(wsse=security)
                    
                    #res=client.service.GetDeviceInformation()
                    
                    
                    #_logger.debug('WSDLXXXX : %s ', res)
                    lg_element = '<wsse:Security><wsse:UsernameToken><wsse:Username>20378890161MODDATOS</wsse:Username><wsse:Password>moddatos</wsse:Password></wsse:UsernameToken></wsse:Security>'
                    #lg_element = Element('wsse:UsernameToken')
                    #soapuser_element = Element('Username').setText('20378890161MODDATOS')
                    #soappass_element = Element('Password').setText('moddatos')
                    #lg_element.append(soapuser_element)
                    #lg_element.append(soappass_element)
                    #client.set_options(headers={'key2': 'value'})
                    
                    
                    request = client.service.sendBill(fileName='20378890161-01-F933-5883.zip',contentFile='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')
                    #request.fileName = 
                    #request.contentFile = 
                
                    
                    
                    #_logger.debug('WSDL : %s ', client)
                    _logger.debug('WSDL-Response : %s ', request)
                    
                _logger.debug('Valor a %s with ', invoice.file_factura_xml_send)
        else:
            _logger.debug('Verifique el parametro de sistema de la ruta de archivos de Sunat !')
            
    
    
    @api.multi
    def process_respuesta_sunat(self):
        ruta_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.ruta')]).value
        
        if ruta_sunat!='':
            for invoice in self:
                
                num_ruc_company = invoice.company_id.vat
                cc = invoice.journal_id.sequence_id.code
                serie = invoice.journal_id.sequence_id.prefix
                serie = serie[:4]
                number_invoice = invoice.number
                number_invoice = number_invoice[5:]
                
                # RUTA ENVIO - ARCHIVO ZIP
                envio_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.envio')]).value
                namefilezip = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".zip"
                if os.path.isfile(envio_sunat+namefilezip):                
                    file = open(envio_sunat+namefilezip, "rb")
                    out = file.read()
                    file.close()
                    invoice.file_factura_zip = base64.encodestring(out)
                    invoice.factura_binary_fname_zip = namefilezip
                    self.write({'factura_binary_fname_zip': namefilezip})
                
                # RUTA ENVIO - ARCHIVO XML
                envio_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.envio')]).value
                namefilexml = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".xml"
                if os.path.isfile(envio_sunat+namefilexml):                
                    file = open(envio_sunat+namefilexml, "rb")
                    out = file.read()
                    file.close()
                    invoice.file_factura_xml = base64.encodestring(out)
                    invoice.factura_binary_fname_xml = namefilexml
                    self.write({'factura_binary_fname_xml': namefilexml})
                
                # RUTA ENVIO - ARCHIVO CDR
                envio_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.rpta')]).value
                namefilerpta = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".zip"
                if os.path.isfile(envio_sunat+namefilerpta):              
                    file = open(envio_sunat+namefilerpta, "rb")
                    out = file.read()
                    file.close()
                    invoice.file_factura_cdr = base64.encodestring(out)
                    invoice.factura_binary_fname_cdr = namefilerpta
                    self.write({'factura_binary_fname_cdr': namefilerpta})
                
                 # RUTA ENVIO - ARCHIVO PDF
                envio_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.repo')]).value
                namefilerepo = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".pdf" 
                if os.path.isfile(envio_sunat+namefilerepo):               
                    file = open(envio_sunat+namefilerepo, "rb")
                    out = file.read()
                    file.close()
                    invoice.file_factura_pdf = base64.encodestring(out)
                    invoice.factura_binary_fname_pdf = namefilerepo
                    self.write({'factura_binary_fname_pdf': namefilerepo})
                    self.write({'state': 'open'})
                
        else:
            _logger.debug('Verifique el parametro de sistema de la ruta de archivos de Sunat !')        
    
    
    @api.multi
    def action_invoice_draft(self):
        _logger.debug('Invoice a Borrador %s with ', self._name)
        self.generate_xml_invoice_10()
        res = super(account_invoice, self).action_invoice_draft()
        return res
    
    @api.multi
    def invoice_validate(self):
        _logger.debug('Invoice a Validar %s with ', self._name)
        res = super(account_invoice, self).invoice_validate()
        return res
    
    @api.multi
    def generate_sunat_files(self):
        _logger.debug('SERA 0123456789 >> %s  ')
        if ast.literal_eval(self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr')]).value):
                return self.generate_json_file_invoice()
            
    @api.multi
    def load_sunat_files(self):
        if ast.literal_eval(self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr')]).value):
                return self.process_respuesta_sunat()        