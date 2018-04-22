import json
import logging

import base64
import os
import zipfile

from jinja2 import FileSystemLoader, Environment
from lxml import etree
#Sera12345
#from signxml import xmldsig
#from voluptuous import Schema, Required, All, Length, ALLOW_EXTRA, Optional
from cStringIO import StringIO

_logger = logging.getLogger(__name__)

class Document(object):

    template_name = ''

    def __init__(self, ruc, data, client):
        self._ruc = ruc
        self._data = json.loads(data)
        self._xml = None
        self._document_name = self.generate_document_name()
        self._data.update({
            'document_name': self._document_name,
            'ruc': self._ruc,
            'voucher_number': '{}-{}'.format(self._data['serial'], self._data['correlative'])
        })
        self._data = json.dumps(self._data, sort_keys=False,separators=(',',':'))
        self._client = client
        self._response = None
        self._zip_path = None
        self.in_memory_data = StringIO()
        self.in_memory_zip = zipfile.ZipFile(self.in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
        _logger.debug('Document 0 %s ',self._data)

    def generate_document_name(self):
         _logger.debug('Document 1 ')

    def validate(self):
        _logger.debug('Document 2 ')

    def render(self):
        _logger.debug('Document 3 ')

    def sign(self):
        _logger.debug('Document 4 ')

    def writetofile(self):
        _logger.debug('Document 5 ')

    def prepare_zip(self):
        _logger.debug('Document 6 ')

    def send(self):
        _logger.debug('Document 7 ')
        self._response = self._client.sendBill('20378890161-01-F933-5883.zip','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')

    def process_response(self):
        _logger.debug('Document 8 ')

    def process(self):
        self.validate()
        self.render()
        self.sign()
        self.prepare_zip()
        self.send()
        self.process_response()
        _logger.debug('Document 9 ')
        return self._response


class Invoice(Document):

    template_name = 'invoice.xml'
    voucher_type = ''

    def validate(self):
         _logger.debug('Invoice Validate ')

    def generate_document_name(self):
        """
        Tipo de comprobante
        01: Factura electronica
        03: Boleta de venta
        07: Nota de credito
        08: Nota de debito
        Serie del comprobante
        FAAA: Facturas
        BAAA: Boletas
        """
        # TODO: Add types as constants in diferent classes
        return '{ruc}-{type}-{serial}-{correlative}'.format(
            ruc=self._ruc,
            type=self._data['voucher_type'],
            serial=self._data['serial'],
            correlative=self._data['correlative']
        )
        _logger.debug('Invoice Generate Document ')