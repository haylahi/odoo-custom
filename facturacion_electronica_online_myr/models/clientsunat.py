import suds
import logging
from openerp import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from suds.client import Client
from suds import WebFault
from suds.plugin import MessagePlugin

_logger = logging.getLogger(__name__)


class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        _logger.debug('Cambia namespace')
        soap_env_parent = context.envelope
        #soap_env_parent.set('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
        #modify this line to reliably find the "recordReferences" element
        #context.envelope[1].setPrefix('SOAP-ENV')
        #context.envelope[1][0].setPrefix('nsenzito0')
        #context.envelope[1][0][0].setPrefix('nsricardo0')

class Clientsunat(object):

    def __init__(self, username, password, debug=False):
        _logger.debug('ClientSunat init ')
        self._username = username
        self._password = password
        self._debug = debug
        self._connect()

    def _connect(self):
        #Produccionxxyyyyy
        #client = Client(url='https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl',plugins=[MyPlugin()])

        #Pruebas
        self._client = Client(url='https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl',plugins=[MyPlugin()])
        security =  suds.wsse.Security()
        token =  suds.wsse.UsernameToken(self._username, self._password)
        security.tokens.append(token)
        self._client.set_options(wsse=security)
        _logger.debug('ClientSunat Connect ')

    def _call_service(self, name, params):
        try:
            #_logger.debug('PARAMS >> %s  ', str(params))
            request = self._client.service.sendBill(**params)
        except WebFault, f:
            _logger.debug('ERROR WEBFAULT >> %s  ', str(f.fault))
            raise UserError(_('SUNAT Respuesta : ' + str(f.fault)))
                
        except Exception, e: 
            _logger.debug('ERROR GENERAL >> %s  ', str(e))
            raise UserError(_('SUNAT Respuesta : ' + str(e)))
    
        #_logger.debug('ClientSunat Response %s >> ',request)
        return request
    
    def sendBill(self, filename, contentfilex):
        """
        Recibe un archivo zip con un unico documento XML de comprobante.
        Devuelve un archivo zip con un documento XML que es la constancia de aceptacion o rechazo.
        """
        params = {
            'fileName': filename,
            'contentFile': contentfilex,
        }
        
        _logger.debug('ClientSunat SendBill ')
        return self._call_service('sendBill',params)