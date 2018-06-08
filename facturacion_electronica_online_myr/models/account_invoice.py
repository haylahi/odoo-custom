# -*- coding: utf-8 -*-
import logging
import json
import ast
import io
import base64
import os.path
import suds
from openerp import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from suds.client import Client
from suds import WebFault
from suds.plugin import MessagePlugin
from lxml import etree
import lxml.etree
from lxml.etree import Element, SubElement
from clientsunat import Clientsunat
from document import Invoice
from datetime import datetime
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from cStringIO import StringIO


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
    
    x_file_factura_xml_send = fields.Binary('Descargar Archivo XML Sunat')
    x_factura_binary_fname_xml_send = fields.Char('Archivo XML Sunat')
    
    x_file_factura_zip = fields.Binary('Respuesta Sunat ZIP')
    x_factura_binary_fname_zip = fields.Char('Archivo ZIP Sunat')
    
    x_file_factura_cdr = fields.Binary('Respuesta Sunat')
    x_factura_binary_fname_cdr = fields.Char('Archivo CDR Sunat')
    
    
    
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
    def generate_data_invoice(self, invoice):
        lines = []
        res_partner = self.env['res.partner'].browse(invoice.partner_id)
        num_ruc_company = invoice.company_id.vat
        cc = str(invoice.journal_id.sequence_id.code)
        serie = invoice.journal_id.sequence_id.prefix
        #serie = invoice.journal_id.code
        serie = serie[:4]
        number_invoice = str(invoice.number)
        pos = number_invoice.rfind('/') + 1
        extracnumberinvoice = number_invoice[pos:] 
        number_invoice = extracnumberinvoice
                
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
            _logger.debug('SERA 37 >> %s  ', cc)
            
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
            format_mtoPrecioVentaItem = '%.2f' % mtoPrecioVentaItem  
            
            #Precio de venta por item
            format_mtoValorVentaItem = '%.2f' % (mtoPrecioVentaItem + mtoIgvItem)  
            
            lines.append({
                        'unit_code': codUnidadMedida,
                        'quantity':quantity,
                        'codProducto':line.product_id.default_code,
                        'description':desItem,
                        'price':price_unit,
                        'mtoIgvItem': format_mtoIgvItem,
                        'tipAfeIGV':tipAfeIGV,
                        'tipSisISC':tipSisISC,
                        'mtoIscItem': format_mtoIscItem,
                        'mtoPrecioVentaItem':format_mtoPrecioVentaItem,
                        'mtoValorVentaItem':format_mtoValorVentaItem
                     })

        
        #Caculos por totales
        
        #Tipo de usuario - Catalogo 6
        tipDocUsuario = invoice.partner_id.catalog_06_id.code
        
        #Num documento de usuario
        _logger.debug('RUC con Error %s' , invoice.partner_id.vat)
        if (invoice.partner_id.vat == False) :
            #numDocUsuario = "00000000000"
            msg = 'Verifique el número de RUC o DNI del cliente a cual le esta emitiendo el documento fiscal.'
            raise ValidationError(_(msg))
        else :
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
        
        
        supplier =  {
                        'ruc':self.company_id.vat,
                        'registration_name':self.company_id.name,
                        'commercial_name':self.company_id.company_registry,
                        'address': {
                            'ubigeo': self.company_id.zip,
                            'street': self.company_id.street,
                            'district': self.company_id.street2,
                            'provincia': self.company_id.city,
                            'departamento': self.company_id.state_id.name,
                            'country_code': self.company_id.country_id.code
                        }
                     }
        
        customer =  {
                        'numDocUsuario':numDocUsuario,
                        'tipDocUsuario':tipDocUsuario,
                        'rznSocialUsuario':rznSocialUsuario
                     }
        
        datos = {
               'issue_date': datetime.today().strftime('%Y-%m-%d'),
               'supplier' : supplier,
               'customer' : customer,
               'correlative':number_invoice, 
               'serial':serie, 
               'voucher_type':cc, 
               'fecEmision': invoice.date_invoice,
               'currency':tipMoneda,
               'mtoOperGravadas': amount_untaxed,
               'mtoOperInafectas':'0.00',
               'mtoOperExoneradas':'0.00',
               'mtoIGV': amount_tax,
               'mtoImpVenta': amount_total,
               'lines': lines
              
            }
                
        return json.dumps(datos, sort_keys=False,separators=(',',':'))
        
    
    @api.multi
    def generate_xml_invoice_10(self):
        ruta_sunat = self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr.ruta')]).value
        if ruta_sunat!='':
            for invoice in self:
                _data = self.generate_data_invoice(invoice)
                
                cc = str(invoice.journal_id.sequence_id.code)
                serie = invoice.journal_id.sequence_id.prefix
                #serie = invoice.journal_id.code
                serie = serie[:4]
                number_invoice = str(invoice.number)
                pos = number_invoice.rfind('/') + 1
                extracnumberinvoice = number_invoice[pos:] 
                number_invoice = extracnumberinvoice
                
                _logger.debug('Invoice Serial %s' , serie)
                _logger.debug('Invoice correlative %s' , number_invoice)
                _logger.debug('Invoice voucher type %s' , cc)
                _logger.debug('JSON a ser enviado para convertir a XML %s' , _data)
                doc = Invoice(self.company_id.vat, _data , Clientsunat('20378890161MODDATOS','MODDATOS', True))
                _cdr_sunat = doc.process()
                _logger.debug('XML Firmado %s' , doc._xml)
                _logger.debug('CDR Sunat %s' , _cdr_sunat)
                _logger.debug('Nombre Archivo %s' , doc._document_name)
               
                
                self.process_respuesta_sunat(invoice,_cdr_sunat, doc._xml,doc._document_name)
        else:
            _logger.debug('Verifique el parametro de sistema de la ruta de archivos de Sunat !')
    
    def base64ToString(self,b):
        return base64.b64decode(b).decode('utf-8')
    
    def buscaDigestValue(self,data,searchTXT):
        root = lxml.etree.parse(StringIO(data))
        str = 'Procesamiento de XML no aceptado - Codigo 27117301'
        for element in root.iter():
            strDigesValue = element.tag 
            if (strDigesValue.find(searchTXT) > 0):
                _logger.debug("CDR Sunat %s %s - %s" % (searchTXT,element.tag, element.text))
                str = element.text
        return str
    
    @api.multi
    def process_respuesta_sunat(self, invoice, _cdr_sunat, xml_firmado,_document_name):
        #Graba CDR en base de datos
        #namefilerpta = num_ruc_company + "-" + cc + "-" + serie + "-" + number_invoice +".zip"
        
        #namefilersend = self.company_id.vat +'-01-F933-5883.xml'
        namefilersend = _document_name +'.xml'
        #namefilerpta = 'R-'+self.company_id.vat+'-01-F933-5883.zip'
        namefilerpta = 'R-'+_document_name+'.zip'
        #namefilerptaXML = 'R-'+self.company_id.vat+'-01-F933-5883.xml'
        namefilerptaXML = 'R-'+_document_name+'.xml'
        strXML = ZipFile(io.BytesIO(base64.b64decode(_cdr_sunat)))
        data = strXML.read(namefilerptaXML)
        _logger.debug('CDR Sunat XML %s' , data)
        
        # RUTA ENVIO - ARCHIVO CDR
        invoice.x_file_factura_cdr = base64.encodestring(data)
        invoice.x_factura_binary_fname_cdr = namefilerptaXML
        invoice.x_cdr_digestvalue = self.buscaDigestValue(data,"DigestValue")
        invoice.x_cdr_description = self.buscaDigestValue(data,"Description")
        self.write({'x_factura_binary_fname_cdr': namefilerptaXML})       
        
        # RUTA ENVIO - ARCHIVO ZIP DE RESPUESTA CON CDR DE SUNAT
        invoice.x_file_factura_zip = base64.encodestring(base64.b64decode(_cdr_sunat))
        invoice.x_factura_binary_fname_zip = namefilerpta
        self.write({'x_factura_binary_fname_zip': namefilerpta})
        
        # RUTA ENVIO - ARCHIVO ZIP FIRMADO ENVIADO A SUNAT
        invoice.x_file_factura_xml_send = base64.encodestring(xml_firmado)
        invoice.x_factura_binary_fname_xml_send = namefilersend
        self.write({'x_factura_binary_fname_xml_send': namefilersend})
                    
    
    
    @api.multi
    def action_invoice_draft(self):
        _logger.debug('Invoice a Borrador %s with ', self._name)
        #self.generate_xml_invoice_10()
        res = super(account_invoice, self).action_invoice_draft()
        return res
    
    @api.multi
    def invoice_validate(self):
        _logger.debug('Invoice a Validar %s with ', self._name)
        self.generate_xml_invoice_10()
        res = super(account_invoice, self).invoice_validate()
        return res
            
    @api.multi
    def load_sunat_files(self):
        if ast.literal_eval(self.env['ir.config_parameter'].search([('key','=','facturacion_electronica.myr')]).value):
                return self.process_respuesta_sunat()        