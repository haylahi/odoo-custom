# -*- coding: utf-8 -*-
import logging
import json
import ast
from openerp import api, fields, models, _


_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    cdr_digestvalue  = fields.Char('Sunat DigestValue')
    
    @api.model
    def _get_default_17(self):
        res = self.env['einvoice.catalog.17'].search([('code','=','01')])
        return res.id or False
    x_code_catalog_17 = fields.Many2one('einvoice.catalog.17',string='Tipo de Operación',help='Seleccione el Tipo de Operación', default=_get_default_17)
    
    @api.model
    def _get_default_07(self):
        res = self.env['einvoice.catalog.07'].search([('code','=','10')])
        return res.id or False
    x_code_catalog_07 = fields.Many2one('einvoice.catalog.07',string='Tipo de IGV',help='Seleccione el Tipo de IGV', default=_get_default_07)


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    
    @api.model
    def _get_default_07(self):
        res = self.env['einvoice.catalog.07'].search([('code','=','10')])
        return res.id or False
    x_code_catalog_07 = fields.Many2one('einvoice.catalog.07',string='Tipo de IGV',help='Seleccione el Tipo de IGV', default=_get_default_07)
    
    x_code_catalog_08 = fields.Many2one('einvoice.catalog.08',string='Tipo de ISC',help='Seleccione el Tipo de ISC')
    
